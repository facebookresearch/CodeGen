# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import os

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss, MSELoss
from transformers.modeling_outputs import SequenceClassifierOutput
from transformers.models.roberta.modeling_roberta import RobertaClassificationHead
from codegen_sources.model.src.model.transformer import (
    TransformerModel,
    create_position_ids_from_input_ids,
)
from logging import getLogger

logger = getLogger()


class ModelConfig:
    def __init__(self, params, num_labels=None, dico=None, **kwargs):
        super().__init__(**kwargs)
        self.num_labels = num_labels
        self.n_langs = params["n_langs"]
        self.n_words = params["n_words"]
        # create fake dico because need in transfo constructor, but not used here.
        # TODO -> do it cleaner way for opensourcing
        self.dico = ["" for i in range(self.n_words)] if dico is None else dico
        self.vocab_size = self.n_words
        self.eos_index = params["eos_index"]
        self.pad_index = params["pad_index"]
        self.id2lang = params["id2lang"]
        self.lang2id = params["lang2id"]
        self.emb_dim_encoder = params["emb_dim_encoder"]
        self.emb_dim_decoder = params["emb_dim_decoder"]
        self.n_heads = params["n_heads"]
        self.n_layers_encoder = params["n_layers_encoder"]
        self.n_layers_decoder = params["n_layers_decoder"]
        self.dropout = params["dropout"]
        self.attention_dropout = params["attention_dropout"]
        self.sinusoidal_embeddings = params["sinusoidal_embeddings"]
        self.spans_emb_encoder = False
        self.gelu_activation = params["gelu_activation"]
        self.share_inout_emb = params["share_inout_emb"]
        self.roberta_mode = getattr(params, "roberta_mode", False)
        # needed for some of the tasks
        self.hidden_size = self.emb_dim_encoder
        self.hidden_dropout_prob = self.dropout
        self.num_attention_heads = self.n_heads
        self.torchscript = False

    @classmethod
    def from_pretrained(
        self, config_path, cache_dir=None, num_labels=None, finetuning_task=None
    ):
        assert os.path.exists(
            config_path
        ), f"cannot reload config : cannot find {config_path}"
        print(config_path)
        reloaded = torch.load(config_path)
        assert (
            "params" in reloaded.keys()
        ), f"params not found in the file {config_path}"
        params_reloaded = reloaded["params"]
        return ModelConfig(params_reloaded, num_labels)


class Pooler(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.emb_dim_encoder, config.emb_dim_encoder)
        self.activation = nn.Tanh()

    def forward(self, hidden_states):
        # We "pool" the model by simply taking the hidden state corresponding
        # to the first token.
        first_token_tensor = hidden_states[:, 0]
        pooled_output = self.dense(first_token_tensor)
        pooled_output = self.activation(pooled_output)
        return pooled_output


class Model(nn.Module):
    def __init__(self, config, lang, is_encoder, add_pooling_layer=True):
        super(Model, self).__init__()
        self.is_encoder = is_encoder
        self.transformer = TransformerModel(config, config.dico, self.is_encoder, True)
        self.lang = lang
        # embeddings is useful for finetuning in encoder-decoder archi
        self.embeddings = ModelEmbeddings(
            self.transformer.roberta_mode,
            self.transformer.lang2id,
            self.transformer.pad_index,
            self.lang,
            self.transformer.embeddings,
            self.transformer.position_embeddings,
            self.transformer.lang_embeddings,
            self.transformer.layer_norm_emb,
            self.transformer.dropout,
        )
        self.pooler = Pooler(config) if add_pooling_layer else None

    def reload_model(self, model_path):
        assert os.path.exists(
            model_path
        ), f"cannot reload model : cannot find {model_path}"
        reloaded = torch.load(model_path)
        model_type = "encoder" if self.is_encoder else "decoder"
        if not (model_type in reloaded.keys() or "model" in reloaded.keys()):
            print(
                f"cannot find encoder nor model in the file {model_path}, do not reload ,model"
            )
            return
        model_reloaded = (
            reloaded[model_type] if model_type in reloaded.keys() else reloaded["model"]
        )
        if all([k.startswith("module.") for k in model_reloaded.keys()]):
            model_reloaded = {k[len("module.") :]: v for k, v in model_reloaded.items()}
        self.transformer.load_state_dict(model_reloaded, strict=True)

    def forward(self, input_ids, attention_mask):
        attention_mask = None  # not use, only here to match HF interface
        bs = input_ids.shape[0]
        lengths = torch.tensor(
            (input_ids != self.transformer.pad_index).sum(dim=1).long()
        )
        input_ids = input_ids.transpose(0, 1)
        lang_id = (
            self.transformer.lang2id[self.lang]
            if self.lang in self.transformer.lang2id
            else self.transformer.lang2id[self.lang.split("_")[0]]
        )
        langs = input_ids.clone().fill_(lang_id)
        output = self.transformer(
            "fwd", x=input_ids, lengths=lengths, langs=langs, causal=False
        ).transpose(0, 1)
        assert output.shape[0] == bs and output.shape[2] == self.transformer.dim
        pooled_output = self.pooler(output) if self.pooler is not None else None
        assert (
            pooled_output.shape[0] == bs
            and pooled_output.shape[1] == self.transformer.dim
        )
        return output, self.pooler(output), None


class ModelJava(Model):
    def __init__(self, config, is_encoder):
        super().__init__(config=config, lang="java_obfuscated", is_encoder=is_encoder)

    @classmethod
    def from_pretrained(
        self, model_path, from_tf=None, config=None, cache_dir=None, is_encoder=True
    ):
        model = ModelJava(config, is_encoder)
        model.reload_model(model_path)
        return model


class ModelJavaFunc(Model):
    def __init__(self, config, is_encoder):
        super().__init__(
            config=config, lang="java_obfuscated_func", is_encoder=is_encoder
        )

    @classmethod
    def from_pretrained(
        self, model_path, from_tf=None, config=None, cache_dir=None, is_encoder=True
    ):
        model = ModelJavaFunc(config, is_encoder)
        model.reload_model(model_path)
        return model


class ModelPython(Model):
    def __init__(self, config, is_encoder):
        super().__init__(config=config, lang="python_obfuscated", is_encoder=is_encoder)

    @classmethod
    def from_pretrained(
        self, model_path, from_tf=None, config=None, cache_dir=None, is_encoder=True
    ):
        model = ModelPython(config, is_encoder)
        model.reload_model(model_path)
        return model


class ModelPythonFunc(Model):
    def __init__(self, config, is_encoder):
        super().__init__(
            config=config, lang="python_obfuscated_func", is_encoder=is_encoder
        )

    @classmethod
    def from_pretrained(
        self, model_path, from_tf=None, config=None, cache_dir=None, is_encoder=True
    ):
        model = ModelPythonFunc(config, is_encoder)
        model.reload_model(model_path)
        return model


class ModelEmbeddings(nn.Module):
    def __init__(
        self,
        roberta_mode,
        lang2id,
        pad_index,
        lang,
        word_embeddings,
        position_embeddings,
        lang_embeddings,
        layer_norm_emb,
        dropout,
    ):
        super().__init__()
        self.lang2id = lang2id
        self.lang = lang
        self.pad_index = pad_index
        self.word_embeddings = word_embeddings
        self.position_embeddings = position_embeddings
        self.lang_embeddings = lang_embeddings
        self.layer_norm_emb = layer_norm_emb
        self.dropout = dropout
        self.roberta_mode = roberta_mode

    def forward(self, input_ids):
        bs, slen = input_ids.size()

        lang_id = (
            self.lang2id[self.lang]
            if self.lang in self.lang2id
            else self.lang2id[self.lang.split("_")[0]]
        )
        langs = input_ids.clone().fill_(lang_id)

        if self.roberta_mode:
            positions = create_position_ids_from_input_ids(input_ids, self.pad_index)
        else:
            positions = input_ids.new(slen).long()
            positions = torch.arange(slen, out=positions).unsqueeze(0)
        tensor = self.word_embeddings(input_ids)
        tensor = tensor + self.position_embeddings(positions).expand_as(tensor)
        tensor = tensor + self.lang_embeddings(langs)
        tensor = self.layer_norm_emb(tensor)
        tensor = F.dropout(tensor, p=self.dropout, training=self.training)

        assert tensor.size() == (bs, slen, self.word_embeddings.embedding_dim), print(
            f"{tensor.size()}"
        )
        return tensor


class ClassificationHead(nn.Module):
    """Head for sentence-level classification tasks."""

    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(config.hidden_dropout_prob)
        self.out_proj = nn.Linear(config.hidden_size, config.num_labels)

    def forward(self, features, **kwargs):
        x = features[:, 0, :]  # take <s> token (equiv. to [CLS])
        x = self.dropout(x)
        x = self.dense(x)
        x = torch.tanh(x)
        x = self.dropout(x)
        x = self.out_proj(x)
        return x


class ModelForSequenceClassification(nn.Module):
    def __init__(self, config, lang):
        super().__init__()
        self.num_labels = config.num_labels
        self.config = config
        if not hasattr(config, "use_return_dict"):
            config.use_return_dict = False
        self.model = Model(config, lang, True)
        self.classifier = RobertaClassificationHead(config)

    def forward(
        self,
        input_ids=None,
        attention_mask=None,
        token_type_ids=None,
        position_ids=None,
        head_mask=None,
        inputs_embeds=None,
        labels=None,
        output_attentions=None,
        output_hidden_states=None,
        return_dict=None,
    ):
        r"""
        labels (:obj:`torch.LongTensor` of shape :obj:`(batch_size,)`, `optional`):
            Labels for computing the sequence classification/regression loss. Indices should be in :obj:`[0, ...,
            config.num_labels - 1]`. If :obj:`config.num_labels == 1` a regression loss is computed (Mean-Square loss),
            If :obj:`config.num_labels > 1` a classification loss is computed (Cross-Entropy).
        """
        return_dict = (
            return_dict if return_dict is not None else self.config.use_return_dict
        )

        outputs = self.model(input_ids, attention_mask=attention_mask,)
        sequence_output = outputs[0]
        logits = self.classifier(sequence_output)

        loss = None
        if labels is not None:
            if self.num_labels == 1:
                #  We are doing regression
                loss_fct = MSELoss()
                loss = loss_fct(logits.view(-1), labels.view(-1))
            else:
                loss_fct = CrossEntropyLoss()
                loss = loss_fct(logits.view(-1, self.num_labels), labels.view(-1))

        if not return_dict:
            output = (logits,) + outputs[2:]
            return ((loss,) + output) if loss is not None else output

        return SequenceClassifierOutput(
            loss=loss,
            logits=logits,
            hidden_states=outputs.hidden_states,
            attentions=outputs.attentions,
        )

    def save_pretrained(self, save_directory):
        """
        Save a model and its configuration file to a directory, so that it can be re-loaded using the
        `:func:`~transformers.PreTrainedModel.from_pretrained`` class method.
        Arguments:
            save_directory (:obj:`str`):
                Directory to which to save. Will be created if it doesn't exist.
        """
        WEIGHTS_NAME = "pytorch_model.bin"

        if os.path.isfile(save_directory):
            print(f"{save_directory} is a file, not a directory. Cannot save model.")
            return
        os.makedirs(save_directory, exist_ok=True)

        # Only save the model itself if we are using distributed training
        model_to_save = self.module if hasattr(self, "module") else self

        state_dict = model_to_save.state_dict()

        # If we save using the predefined names, we can load using `from_pretrained`
        output_model_file = os.path.join(save_directory, WEIGHTS_NAME)

        # model_to_save.config.save_pretrained(save_directory)
        torch.save(state_dict, output_model_file)


class ModelForSequenceClassificationPython(ModelForSequenceClassification):
    def __init__(self, config):
        super().__init__(config=config, lang="python_obfuscated")

    @classmethod
    def from_pretrained(self, model_path, from_tf=None, config=None, cache_dir=None):
        model = ModelForSequenceClassificationPython(config)
        model.model.reload_model(model_path)
        return model


class ModelForSequenceClassificationJava(ModelForSequenceClassification):
    def __init__(self, config):
        super().__init__(config=config, lang="java_obfuscated")

    @classmethod
    def from_pretrained(self, model_path, from_tf=None, config=None, cache_dir=None):
        model = ModelForSequenceClassificationJava(config)
        model.model.reload_model(model_path)
        return model
