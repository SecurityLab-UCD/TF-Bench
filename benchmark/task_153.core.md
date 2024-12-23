
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromIntegral

# poly_type
Ad-hoc

# signature
```haskell
fromIntegral :: (Integral a, Num b) => a -> b
```   

# code
```haskell
fromIntegral = fromInteger . toInteger
```

# dependencies
## 0
```haskell
fromInteger :: Num a => Integer -> a
```
## 1
```haskell
toInteger :: Integral a => a -> Integer
```
## 2
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
