
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--decodeFloat-Double

# poly_type
Monomorphic

# signature
```haskell
decodeFloat :: Double -> (Integer, Int)
```   

# code
```haskell
decodeFloat (D# x#) = case integerDecodeDouble# x#   of
                      (# i, j #) -> (i, I# j)
```

# dependencies
## 0
```haskell
D# :: Double# -> Double
```
## 1
```haskell
integerDecodeDouble# :: Double# -> (# Integer, Int# #)
```
## 2
```haskell
I# :: Int# -> Int
```