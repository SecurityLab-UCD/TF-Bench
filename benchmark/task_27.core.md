
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromRational

# poly_type
Ad-hoc

# signature
```haskell
fromRational :: Fractional a => Rational -> a
```   

# code
```haskell
fromRational (x:%y) = fromInteger x % fromInteger y
```

# dependencies
## 0
```haskell
fromInteger :: Num a => Integer -> a
```
## 1
```haskell
(%) :: (Integral a) => a -> a -> Ratio a
```
## 2
```haskell
(:%) :: Integer -> Integer -> Rational
```
