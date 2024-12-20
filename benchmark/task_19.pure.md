
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--quot

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 => a -> a -> a
```   

# code
```haskell
f1 n d = f2 (f3 n d)
```

# dependencies
## 0
```haskell
f2 :: (a, b) -> a
```
## 1
```haskell
f3 :: T1 => a -> a -> (a, a)
```
