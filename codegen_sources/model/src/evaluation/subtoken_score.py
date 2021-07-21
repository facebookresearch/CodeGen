# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import os

from stringcase import snakecase

from ..utils import read_file_lines


def compute_subtokens(token):
    return [x for x in snakecase(token).split("_") if len(x) > 0]


def subtoken_counts(proposed, ground_truth):
    """
    Compute the number of precise tokens, proposed tokens and ground truth tokens
    from two strings representing tokens.
    """
    gt_subtokens = set(compute_subtokens(ground_truth))
    proposed_subtokens = set(compute_subtokens(proposed))
    precise_subtokens = proposed_subtokens.intersection(gt_subtokens)
    return len(precise_subtokens), len(proposed_subtokens), len(gt_subtokens)


def subtoken_scores(proposed, ground_truth):
    precise, proposed, gt = subtoken_counts(proposed, ground_truth)
    precision = precise / proposed if proposed > 0 else 0
    recall = precise / gt if gt > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0
    return precision, recall, f1


def run_subtoken_score(ref, hyp, subtoken_average=False, all_beams=False):
    """
    Given a file of hypothesis and reference files,
    evaluate the subtoken-level precision and recall
    """
    if all_beams:
        assert not subtoken_average
    for h in hyp:
        assert os.path.isfile(h), f"file {h} does not exist"
    assert os.path.isfile(ref) or os.path.isfile(ref + "0")
    refs = read_file_lines(ref)
    hyps = list(zip(*[read_file_lines(path) for path in hyp]))
    if subtoken_average:
        return subtoken_score_on_lines_subtoken_level([h[0] for h in hyps], refs)
    else:
        if not all_beams:
            hyps = [[h[0]] for h in hyps]
        assert len(hyps) == len(refs)
        return subtoken_score_on_lines(hyps, refs)


def subtoken_score_on_lines(hyps_list, refs):
    precisions, recalls, f1_scores = [], [], []
    count_exact_matches = 0
    for hyps, ref in zip(hyps_list, refs):
        matches = {}
        for obfuscated, deobfuscated in [
            (entry.strip().split(" ")[0], entry.strip().split(" ")[1])
            for entry in ref.split("|")
        ]:
            assert obfuscated not in matches
            matches[obfuscated] = {"ref": deobfuscated}
        for hyp_index, hyp in enumerate(hyps):
            for entry in hyp.split("|"):
                split = entry.strip().split(" ")
                if len(split) < 2:
                    continue
                else:
                    obfuscated, deobfuscated = split[0], split[1]
                if obfuscated not in matches:
                    # the model is trying to deobfuscate a variable that does not exist. It can be detected automatically and ignored
                    continue
                else:
                    matches[obfuscated][f"hyp_{hyp_index}"] = deobfuscated
        for match in matches.values():
            assert "ref" in match
            best_precision, best_recall, best_f1 = 0, 0, 0
            exact_match = False
            for k, v in match.items():
                if k.startswith("hyp"):
                    if v == match["ref"]:
                        exact_match = True
                    precision, recall, f1 = subtoken_scores(v, match["ref"])
                    if f1 > best_f1:
                        best_precision, best_recall, best_f1 = precision, recall, f1

            precisions.append(best_precision)
            recalls.append(best_recall)
            f1_scores.append(best_f1)
            count_exact_matches += 1 if exact_match else 0
    nb_tokens = len(precisions)
    assert (
        nb_tokens == len(precisions) == len(recalls) == len(f1_scores)
    ), "all lists should have the same size"
    precision = sum(precisions) / nb_tokens if nb_tokens > 0 else 0
    recall = sum(recalls) / nb_tokens if nb_tokens > 0 else 0
    f1 = sum(f1_scores) / nb_tokens if nb_tokens > 0 else 0
    ratio_exact_matches = count_exact_matches / nb_tokens if nb_tokens > 0 else 0
    return {
        "precision": precision,
        "recall": recall,
        "F1": f1,
        "exact_match": ratio_exact_matches,
    }


def subtoken_score_on_lines_subtoken_level(hyps, refs):
    precise_subtokens, proposed_subtokens, gt_subtokens = 0, 0, 0
    for hyp, ref in zip(hyps, refs):
        matches = {}
        for obfuscated, deobfuscated in [
            (entry.strip().split(" ")[0], entry.strip().split(" ")[1])
            for entry in ref.split("|")
        ]:
            assert obfuscated not in matches
            matches[obfuscated] = {"ref": deobfuscated}
        for entry in hyp.split("|"):
            split = entry.strip().split(" ")
            if len(split) < 2:
                continue
            else:
                obfuscated, deobfuscated = split[0], split[1]
            if obfuscated not in matches:
                # the model is trying to deobfuscate a variable that does not exist. It can be detected automatically and ignored
                continue
            else:
                matches[obfuscated]["hyp"] = deobfuscated
        for match in matches.values():
            assert "ref" in match
            precise, proposed, gt = subtoken_counts(match.get("hyp", ""), match["ref"])
            precise_subtokens += precise
            proposed_subtokens += proposed
            gt_subtokens += gt
    precision = precise_subtokens / proposed_subtokens if proposed_subtokens > 0 else 0
    recall = precise_subtokens / gt_subtokens if gt_subtokens > 0 else 0
    return {
        "precision": precision,
        "recall": recall,
        "F1": 2 * precision * recall / (precision + recall)
        if precision + recall > 0
        else 0,
    }
