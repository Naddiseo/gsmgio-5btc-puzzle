# Zden, cryptopuzle LVL.5. "...sum of two ~~consecutive~~ following rectangles..."

This puzzle composed by Zden and published on his site [[1]](https://crypto.haluska.sk/) [[1']](https://crypto.haluska.sk/crypto5fix.png). 
This guy (or girl) known for constructing, funding and publishing different mostly algorithmical CryptoPuzzles (better check his site to 
understand what i mean). LVL5 (described here) is one of his yet unsolved puzzles.

The puzzle is stated to hold ***0.0055 BTC (~ 150$)*** - [1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7](https://www.blockchain.com/explorer/addresses/btc/1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7)

First time, this puzzle was published at the end of 2018 year. ***Puzzle represented by a single *.PNG file*** and a statement: 
"Level 5 - Find the private key in this image" [[1''']](https://twitter.com/Zd3N/status/1060955171591766018).


Later in December of 2018, the Original Twitter hint was released [[2]](https://twitter.com/Zd3N/status/1077146640090316800):
```
Puzzles' Hints Xmas Bundle. <BTCrypto L5> Sum of two consecutive following rectangles areas creates one byte of the private key.
Apply more operations to obtain the results in byte range. <XIXOIO> Byte 0x77 is part of the private key. #HPPXMS Good luck! [/64] [#12]
```
Here i guess, only ```Sum of two consecutive following rectangles areas creates one byte of the private key. 
Apply more operations to obtain the results in byte range.``` related to LVL5 puzzle.


But later, after several years of puzzle being unsolved, ***the author released the update*** for puzzle with a statement: 
"UNSOLVED for over 3 years because the original release was uncomplete! Relaunched on 12th of December 2021. My excuses to everyone!

Past hint.
(clarity edit: sum of two  ~~consecutive~~ following rectangles...)
"
![FIXED LVL5 puzzle](https://github.com/HomelessPhD/Zden_LVL5/blob/c82beb668696d7f59aca16465ce408747a240b88/crypto5fix.png)

Author ***crossed out word*** ```consecutive``` from the hint AND ***added*** several elements to the picture: ***white line under the rectangle #40 with 17
pixel length***, ***white line under the rectangle #53 with 6 pixel length***, the ***minipuzzle-HINT in the left bottom corner*** of the image that is 
shown below:

![LVL5 interesting spots](https://github.com/HomelessPhD/Zden_LVL5/blob/6bdb5f55b918f7c589a55f906ba96ca16379ded4/pics/crypto5fix_valuableSpots.png)


## HINTS

Original hint from twitter with a correction given on the author site:

 **Sum of two ~~consecutive~~ following rectangles areas creates one byte of the private key.
Apply more operations to obtain the results in byte range.**

Hint mini-puzzle from the picture:
![mini-puzzle hint](https://github.com/HomelessPhD/Zden_LVL5/blob/6bdb5f55b918f7c589a55f906ba96ca16379ded4/pics/crypto5fix_BigHint.png)

LXIV is 64 written in Roman Numeral notation - number closely related to puzzle....

This small picture could represent the arcitercture of each rectangle pointing the math behind rectangular objects geometry (sizes, width, heigh,...)
...maybe we should think of the "text" in this hint-picture as formula: ***[-1 * 10 + 64 /*/]*** or ***[-1 * x + 64 /x/]*** ???

What about the numbers: 8 digits than "FIX" and another 8 digits.... vector column of 8 elements multiplied to vector row of 8 elements could form
the 8x8 matrix (like the rectangular shaped in the puzzle), or they simply could be i,j - some numbers that should be applied to each column, row:

```
      0,1 0,1 0,1 0,2 0,2 0,1 0,1 0,1
      9,1 9,1 9,1 9,2 9,2 9,1 9,1 9,1
      1,1 1,1 1,1 1,2 1,2 1,1 1,1 1,1
      1,1 1,1 1,1 1,2 1,2 1,1 1,1 1,1
      1,1 1,1 1,1 1,2 1,2 1,1 1,1 1,1
      8,1 8,1 8,1 8,2 8,2 8,1 8,1 8,1
      1,1 1,1 1,1 1,2 1,2 1,1 1,1 1,1
      9,1 9,1 9,1 9,2 9,2 9,1 9,1 9,1
```
May be the numbers in this hint means the begin and end of the private key, like: ***0x09111819????????????????????????????????????????????????11122111*** and given for verification of the solving, but that actually make no sense....

<TO DO - decypher this hint (check previous puzzles from his site to get familliar with such mini-puzzles)>

## IMPORTANT NOTICE
The first thing i considered when saw the puzzle picture was: 64 rectangular shape is like 64 HEX digits of private key and
so each rectangular shape should be somehow evaluated to [0 - 15] integer (HEX digit) to form the resulting private key.

BUT, the hint: ***the sum of two following rectangles areas creates one byte***? If rectangular codes the hex digits two such digits
forms the byte but not as straigh sum - its rather D1*16 + D2 and id not call it a sum. So if the author tried to hint us that this HEX
approach is correct and each rectangles should be interpret as HEX digit so two following digits forms the byte - he made a bad job: after
this hint those who initially could guessed that rectangles form the list of hex digits - would forget about that idea here be cause byte 
is not a sum of hex digits. Thats why i moved to operating on ***SUM OF TWO RECTANGLES AREAS** making a byte - because of this
***the sum of two following rectangles areas creates one byte*** ....

## Evaluation of the areas

BTC private key, in general, is a 256 bit integer value that could be coded by 32 bytes (or 64 hexadecimal digits).
The main object on the puzzle picture is a series of 64 rectangular shells (difference between two cocentric outter and inner rectangles).

The textual hint stated that each byte of private key is composed using "Sum of two ~~consecutive~~ following rectangles areas" 
(my interpretation).

Lets assume the numeration as given on the picture above:
```
      1   2  3  4  5  6  7  8
      9  10 11 12 13 14 15 16
      17 18 19 20 21 22 23 24
      25 26 27 28 29 30 31 32
      33 34 35 36 37 38 39 40
      41 42 43 44 45 46 47 48
      49 50 51 52 53 54 55 56
      57 58 59 60 61 62 63 64
```
Lets introduce some notation: 
  - Outer (O) rectangular is a solid rectangular object bounded by external border of the drawn rectangular shell
    (what the white rectangle could be in case of no black area inside)
  - Inner (I) rectangular is a solid rectangular object bounded by internal border of the drawn rectangular shell
    (the black rectangle - only black pixels)
  - Rectangular shell is the difference between Outer and Inner rectangles - white pixels in between (that is actually
    drawn on the picture)

![Rectangles](https://github.com/HomelessPhD/Zden_LVL5/blob/7397f9e7de2f30295bbab28e4c843ec59fbe303b/pics/A_measure.png)

Measuring the area for each: Outer, Inner, Outer - Inner (rectangular shell) are done via MATLAB code that is attached in 
"Analysis" folder here in github (this code also producec further analysis with Private Key synthesis). 
The results are stored in *.csv file: *_A.csv ("Analysis\Results\").

![measuring](https://github.com/HomelessPhD/Zden_LVL5/blob/6ad1701147e214027a23c48478bce25c20b8d555/pics/measuring.png)

Here i've tried to interpret the white lines under rectangles:
 - prefix "noLine" means i have not counted those 2 lines and areas are counted as is;
 - prefix "minus" means i have substracted the lines length from an appropriate Outer rectangle values
 - prefix "plus" means i have added the lines length to an appropriate Outer rectangle values
 - prefix "multiply" means i have multiplied an appropriate Outer rectangle areas to appropriate lines length

In general, there are numerous ways to traverse this 2D array collecting 32 pairs. I will asssume only 4 options here:
 -  [1 + 2], [3 + 4], [5 + 6], [7 + 8], [9 + 10], ..., [61 + 62], [63 + 64]
 -  [1 + 9], [17 + 25], [33 + 41], [49 + 57], [2 + 10],...., [40 + 48], [56 + 64]
 -  [1 + 9], [2 + 10], [3+11], [4+12],[5+13],[6+14],[7+15],[8+16],[17+25],...,[55+63],[56+64]
 -  [1 + 2], [9+10], [17+18],[25+26],[33+34],[41+42],[49+50],[57+58],[3+4],...,[55+56],[63+64]

I have tried these 4 options - with each rectangle (outter, inner, shell) area - that produced 12 lists of 32 integer
values.

Each resulting value (sume of areas of two rectangles or rectangular shell) in general goes outside of the BYTE (0-255)
values range. Author stated that there is some transformation at the final stage (right now) that should pack this 
integers into byte range. Here we go again, generally speaking there are infinite number of such tranformation exists.
The most obvious are:
 - Modulo operation: INTEGER_NUMBER % 256
 - Dummy normalization: (INTEGER_NUMBER / max_number_in_list) * 255
 - Another normalization: ( (INTEGER_NUMBER-min_number_in_list) / (max_number_in_list - min_number_in_list) )* 255

I tried them all - resulting PrivateKeys (byte list transformed into hexadecimal notation) could be found 
in *_keys.txt files. All produced by the mentioned MATLAB script **crack_pzl.m**

In order to verify resulting keys i composed python script: **CRPT5FIX_checkAddrs.py***
(without address balance verification because the goal address is known. It should be [1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7](https://www.blockchain.com/explorer/addresses/btc/1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7)



## P.S.

Thank you for spending time on my notes, i hope it was not totally useless and you've found something interesting. 

Any ideas\questions or propositions you may send to generalizatorSUB@gmail.com - also look at my twitter @MiningPredict.

-------------------------------------------------------------------------
### References:

[1] Zden cryptopuzles - https://crypto.haluska.sk/

[1'] Zdens' LVL5 cryptopuzle -  https://crypto.haluska.sk/crypto5fix.png

[1'''] Originial puzzle releasing tweet (https://twitter.com/Zd3N/status/1060955171591766018)

[2] Original hint - https://twitter.com/Zd3N/status/1077146640090316800

[@] The prize stated to be here - https://www.blockchain.com/explorer/addresses/btc/1cryptoGeCRiTzVgxBQcKFFjSVydN1GW7

[*] MiningPredict (my twitter page) - https://twitter.com/miningpredict



-------------------------------------------------------------------------
### Support
I am poor Ukrainian student that will really appreciate any donations.
I have no home (flat\appartment), live in the dorm (refugee shelter).
 
P.S. Successfully evacuated from occupied regions of Ukraine.

**BTC**:  `1QKjnfVsTT1KXzHgAFUbTy3QbJ2Hgy96WU`

**LTC**:  `LNQopZ7ozXPQtWpCPrS4mGGYRaE8iaj3BE`

**DOGE**: `DQvfzvVyb4tnBpkd3DRUfbwJjgPSjadDTb`

 **BSV**: `1E56gGQ1rYG4kkRo5qPLMK7PHcpVYj15Pv`

**AR**: `0UM6uoLrrnxXuYpHMBDAv-6txNTMdaEkR2m_bP_1HyE`
(have never used Arweave wallet)
