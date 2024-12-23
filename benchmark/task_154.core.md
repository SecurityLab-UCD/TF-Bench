
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--realToFrac

# poly_type
Ad-hoc

# signature
```haskell
realToFrac :: (Real a, Fractional b) => a -> b
```   

# code
```haskell
realToFrac = fromRational . toRational
```

# dependencies
## 0
```haskell
fromRational :: Fractional a => Rational -> a
```
## 1
```haskell
toRational :: Real a => a -> Rational
```
## 2
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
