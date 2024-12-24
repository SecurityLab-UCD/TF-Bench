
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--encodeFloat-Double

# poly_type
Monomorphic

# signature
```haskell
encodeFloat :: Integer -> Int -> Double
```   

# code
```haskell
encodeFloat i (I# j) = D# (integerEncodeDouble# i j)
```

# dependencies
