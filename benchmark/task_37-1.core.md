
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--encodeFloat-Float

# poly_type
Monomorphic

# signature
```haskell
encodeFloat :: Integer -> Int -> Float
```   

# code
```haskell
encodeFloat i (I# e) = F# (integerEncodeFloat# i e)
```

# dependencies
## 0
```haskell
I# :: Int# -> Int
```
## 1
```haskell
F# :: Float# -> Float
```
## 2
```haskell
integerEncodeFloat# :: Integer -> Int# -> Float#
```