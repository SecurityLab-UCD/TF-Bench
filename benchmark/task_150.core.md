
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--odd

# poly_type
Ad-hoc

# signature
```haskell
odd :: Integral a => a -> Bool
```   

# code
```haskell
odd = not . even
```

# dependencies
## 0
```haskell
not :: Bool -> Bool
```
## 1
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
## 2
```haskell
even :: Integral a => a -> Bool
```