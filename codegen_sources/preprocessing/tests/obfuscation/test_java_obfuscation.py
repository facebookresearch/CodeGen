# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

from codegen_sources.preprocessing.tests.obfuscation.utils import diff_tester
from codegen_sources.preprocessing.lang_processors.java_processor import JavaProcessor
from pathlib import Path

processor = JavaProcessor(root_folder=Path(__file__).parents[4].joinpath("tree-sitter"))


def test_obfuscation_var_definition():
    java_code = """public class Factorial{
     public static Long factorial(Long n){
        Long res = 1L;
        for ( int i = 1; i <= n; ++i) res *= (i + 1);
        return res;
    }
}
        """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
public static Long FUNC_0 ( Long VAR_0 ) {
Long VAR_1 = 1L ;
for ( int VAR_2 = 1 ; VAR_2 <= VAR_0 ; ++ VAR_2 ) VAR_1 *= ( VAR_2 + 1 ) ;
return VAR_1 ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Factorial | FUNC_0 factorial | VAR_0 n | VAR_1 res | VAR_2 i",
        dico,
        split=" | ",
    )


def test_obfuscation_recursive_method():
    java_code = """public class Factorial{
public Long factorial(Long n){
    if (n == 1L) return 1L;
    return n * factorial(n-1);
    }
}
"""
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
public Long FUNC_0 ( Long VAR_0 ) {
if ( VAR_0 == 1L ) return 1L ;
return VAR_0 * FUNC_0 ( VAR_0 - 1 ) ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester("CLASS_0 Factorial | FUNC_0 factorial | VAR_0 n", dico, split=" | ")


def test_obfuscation_identical_names():
    java_code = """
public class HelloWorld{

     public static void main(String []args){
        Factorial factorial = new Factorial();
        System.out.println(factorial.factorial(3L));
     }
}

class Factorial{
    public Long factorial(Long n){
        if (n == 1L) return 1L;
        return n * factorial(n-1);
        }
}"""
    res, dico = processor.obfuscate_code(java_code)

    expected = """public class CLASS_0 {
public static void main ( String [ ] VAR_0 ) {
CLASS_1 VAR_1 = new CLASS_1 ( ) ;
System . out . println ( VAR_1 . FUNC_0 ( 3L ) ) ;
}
}
class CLASS_1 {
public Long FUNC_0 ( Long VAR_2 ) {
if ( VAR_2 == 1L ) return 1L ;
return VAR_2 * FUNC_0 ( VAR_2 - 1 ) ;
}
}
        """

    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 HelloWorld | CLASS_1 Factorial | FUNC_0 factorial | VAR_0 args | VAR_1 factorial | VAR_2 n",
        dico,
        split=" | ",
    )


def test_methods_overloading():
    java_code = """public class Factorial{
     public static Long factorial(Long n, bool verbose){
        Long res = 1L;
        for ( int i = 1; i <= n; ++i) res *= (i + 1);
        if (verbose) System.out.println(res);
        return res;
    }

     public static Long factorial(Long n){
        return factorial(n, 0);
    }
}
        """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
public static Long FUNC_0 ( Long VAR_0 , bool VAR_2 ) {
Long VAR_3 = 1L ;
for ( int VAR_4 = 1 ; VAR_4 <= VAR_0 ; ++ VAR_4 ) VAR_3 *= ( VAR_4 + 1 ) ;
if ( VAR_2 ) System . out . println ( VAR_3 ) ;
return VAR_3 ;
}
public static Long FUNC_0 ( Long VAR_1 ) {
return FUNC_0 ( VAR_1 , 0 ) ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Factorial | FUNC_0 factorial | VAR_0 n | VAR_1 n | VAR_2 verbose | VAR_3 res | VAR_4 i",
        dico,
        split=" | ",
    )


def test_class_constructor_and_attributes():
    java_code = """public class Factorial{
    private Long n;
    public Factorial(Long number){
        this.n = number;
    }
     public Long compute(){
        Long res = 1L;
        for ( int i = 1; i <= this.n; ++i) res *= i;
        return res;
    }
}
        """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
private Long VAR_0 ;
public CLASS_0 ( Long VAR_1 ) {
this . VAR_0 = VAR_1 ;
}
public Long FUNC_0 ( ) {
Long VAR_2 = 1L ;
for ( int VAR_3 = 1 ; VAR_3 <= this . VAR_0 ; ++ VAR_3 ) VAR_2 *= VAR_3 ;
return VAR_2 ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Factorial | FUNC_0 compute | VAR_0 n | VAR_1 number | VAR_2 res | VAR_3 i",
        dico,
        split=" | ",
    )


def test_class_constructor_and_attributes_without_this():
    java_code = """public class Factorial{
        private Long n;
        public Factorial(Long number){
            this.n = number;
        }
         public Long compute(){
            Long res = 1L;
            for ( int i = 1; i <= n; ++i) res *= i;
            return res;
        }
    }
            """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
private Long VAR_0 ;
public CLASS_0 ( Long VAR_1 ) {
this . VAR_0 = VAR_1 ;
}
public Long FUNC_0 ( ) {
Long VAR_2 = 1L ;
for ( int VAR_3 = 1 ; VAR_3 <= VAR_0 ; ++ VAR_3 ) VAR_2 *= VAR_3 ;
return VAR_2 ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Factorial | FUNC_0 compute | VAR_0 n | VAR_1 number | VAR_2 res | VAR_3 i",
        dico,
        split=" | ",
    )


def test_multiple_definitions():
    java_code = """public class Operations{
        public int PlusMinus(int a, int b){
            int sum = a + b, dif = a - b;
            return dif > 0 ? dif : sum;
        }
}
            """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
public int FUNC_0 ( int VAR_0 , int VAR_1 ) {
int VAR_2 = VAR_0 + VAR_1 , VAR_3 = VAR_0 - VAR_1 ;
return VAR_3 > 0 ? VAR_3 : VAR_2 ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Operations | FUNC_0 PlusMinus | VAR_0 a | VAR_1 b | VAR_2 sum | VAR_3 dif",
        dico,
        split=" | ",
    )


def test_handling_scopes():
    java_code = """public class Operations{
        public int sum(int n){
            int res = 0 ;
            for ( int i = 0 ; i < n ; ++ i ) res += i ;
            for ( int i = 0 ; i < n ; ++ i ) res -= i ;
            return res;
        }
}
            """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
public int FUNC_0 ( int VAR_0 ) {
int VAR_1 = 0 ;
for ( int VAR_2 = 0 ; VAR_2 < VAR_0 ; ++ VAR_2 ) VAR_1 += VAR_2 ;
for ( int VAR_3 = 0 ; VAR_3 < VAR_0 ; ++ VAR_3 ) VAR_1 -= VAR_3 ;
return VAR_1 ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Operations | FUNC_0 sum | VAR_0 n | VAR_1 res | VAR_2 i | VAR_3 i",
        dico,
        split=" | ",
    )


def test_constants():
    java_code = """
public class Operations{
    public static final Long LIMIT = 1000L;
    public int sum(int n){
        int res = 0 ;
        for ( int i = 0 ; i < n ; ++ i ) res += i ;

        return res < LIMIT ? res : LIMIT ;
    }
}
            """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
public static final Long VAR_0 = 1000L ;
public int FUNC_0 ( int VAR_1 ) {
int VAR_2 = 0 ;
for ( int VAR_3 = 0 ; VAR_3 < VAR_1 ; ++ VAR_3 ) VAR_2 += VAR_3 ;
return VAR_2 < VAR_0 ? VAR_2 : VAR_0 ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Operations | FUNC_0 sum | VAR_0 LIMIT | VAR_1 n | VAR_2 res | VAR_3 i",
        dico,
        split=" | ",
    )


def test_standard_function():
    java_code = """
public class Operations{
    public int maximum(int a, int b){
        return Math.max(a, b) ;
    }
}
            """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public class CLASS_0 {
public int FUNC_0 ( int VAR_0 , int VAR_1 ) {
return Math . max ( VAR_0 , VAR_1 ) ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Operations | FUNC_0 maximum | VAR_0 a | VAR_1 b", dico, split=" | "
    )


def test_imports():
    java_code = """
import java.io.*;
import java.util.*;

class ArrayListExample {
    public static void main(String[] args)
    {
        int n = 5;
        ArrayList<Integer> arrli = new ArrayList<Integer>(n);

        for (int i = 1; i <= n; i++) arrli.add(i);
        System.out.println(arrli);
        }
}
            """
    res, dico = processor.obfuscate_code(java_code)
    expected = """import java . io . * ;
import java . util . * ;
class CLASS_0 {
public static void main ( String [ ] VAR_0 )
{
int VAR_1 = 5 ;
ArrayList < Integer > VAR_2 = new ArrayList < Integer > ( VAR_1 ) ;
for ( int VAR_3 = 1 ; VAR_3 <= VAR_1 ; VAR_3 ++ ) VAR_2 . add ( VAR_3 ) ;
System . out . println ( VAR_2 ) ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 ArrayListExample | VAR_0 args | VAR_1 n | VAR_2 arrli | VAR_3 i",
        dico,
        split=" | ",
    )


def test_inheritance_with_this():
    # not working perfectly at the moment. get_speed() returns the wrong variable if we remove the "this."
    java_code = """
class Bicycle
{
    public int gear;
    public int speed;

    public Bicycle(int gear, int speed)
    {
        this.gear = gear;
        this.speed = speed;
    }
}

class MountainBike extends Bicycle
{
    public int seatHeight;

    public MountainBike(int gear, int speed, int startHeight)
    {
        super(gear, speed);
        seatHeight = startHeight;
    }
    public int get_speed()
    {
        return this.speed;
    }
}
            """
    res, dico = processor.obfuscate_code(java_code)
    expected = """class CLASS_0
{
public int VAR_0 ;
public int VAR_3 ;
public CLASS_0 ( int VAR_1 , int VAR_4 )
{
this . VAR_0 = VAR_1 ;
this . VAR_3 = VAR_4 ;
}
}
class CLASS_1 extends CLASS_0
{
public int VAR_6 ;
public CLASS_1 ( int VAR_2 , int VAR_5 , int VAR_7 )
{
super ( VAR_2 , VAR_5 ) ;
VAR_6 = VAR_7 ;
}
public int FUNC_0 ( )
{
return this . VAR_3 ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Bicycle | CLASS_1 MountainBike | FUNC_0 get_speed | VAR_0 gear | VAR_1 gear | VAR_2 gear | VAR_3 speed | VAR_4 speed | VAR_5 speed | VAR_6 seatHeight | VAR_7 startHeight",
        dico,
        split=" | ",
    )


def test_inheritance_inverted():
    java_code = """
class MountainBike extends Bicycle
{
    public int seatHeight;

    public MountainBike(int gear, int speed, int startHeight)
    {
        super(gear, speed);
        seatHeight = startHeight;
    }
    public int get_speed()
    {
        return this.speed;
    }
}
class Bicycle
{
    public int gear;
    public int speed;

    public Bicycle(int gear, int speed)
    {
        this.gear = gear;
        this.speed = speed;
    }
}
            """
    res, dico = processor.obfuscate_code(java_code)
    expected = """
class CLASS_0 extends CLASS_1
{
public int VAR_0 ;
public CLASS_0 ( int VAR_1 , int VAR_4 , int VAR_7 )
{
super ( VAR_1 , VAR_4 ) ;
VAR_0 = VAR_7 ;
}
public int FUNC_0 ( )
{
return this . VAR_5 ;
}
}
class CLASS_1
{
public int VAR_2 ;
public int VAR_5 ;
public CLASS_1 ( int VAR_3 , int VAR_6 )
{
this . VAR_2 = VAR_3 ;
this . VAR_5 = VAR_6 ;
}
}
"""
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 MountainBike | CLASS_1 Bicycle | FUNC_0 get_speed | VAR_0 seatHeight | VAR_1 gear | VAR_2 gear | VAR_3 gear | VAR_4 speed | VAR_5 speed | VAR_6 speed | VAR_7 startHeight",
        dico,
        split=" | ",
    )


def test_interfaces():
    java_code = """
public interface LinkFilter {
  public boolean accept ( String url ) ;
}
                """
    res, dico = processor.obfuscate_code(java_code)
    expected = """public interface CLASS_0 {
public boolean FUNC_0 ( String VAR_0 ) ;
}
    """
    diff_tester(expected.strip(), res.strip())
    diff_tester("CLASS_0 LinkFilter | FUNC_0 accept | VAR_0 url", dico, split=" | ")


def test_enums():
    java_code = """
enum Color
{
    RED, GREEN, BLUE;
}
                """
    res, dico = processor.obfuscate_code(java_code)
    expected = """
enum CLASS_0
{
VAR_0 , VAR_1 , VAR_2 ;
}
    """
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Color | VAR_0 RED | VAR_1 GREEN | VAR_2 BLUE", dico, split=" | "
    )


def test_inherited_methods():
    java_code = """
class Vehicle {
    public void honk() {
        System.out.println("Tuut, tuut!");
    }
}

class Car extends Vehicle {
    String y = "sub";
}

public class Test {
    public static void main(String[] args) {
        Car myCar = new Car();
        myCar.honk();  // how is this obfuscated?
    }
}
                """
    res, dico = processor.obfuscate_code(java_code)
    expected = """
class CLASS_0 {
public void FUNC_0 ( ) {
System . out . println ( "Tuut, tuut!" ) ;
}
}
class CLASS_1 extends CLASS_0 {
String VAR_0 = "sub" ;
}
public class CLASS_2 {
public static void main ( String [ ] VAR_1 ) {
CLASS_1 VAR_2 = new CLASS_1 ( ) ;
VAR_2 . FUNC_0 ( ) ;
}
}
    """
    diff_tester(expected.strip(), res.strip())
    diff_tester(
        "CLASS_0 Vehicle | CLASS_1 Car | CLASS_2 Test | FUNC_0 honk | VAR_0 y | VAR_1 args | VAR_2 myCar",
        dico,
        split=" | ",
    )


# TODO: defines
