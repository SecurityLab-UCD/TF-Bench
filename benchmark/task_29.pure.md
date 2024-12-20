
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--truncate

# poly_type
Ad-hoc

# signature
```haskell
f1 :: (T1 a, T2 b) => a -> b
```   

# code
```haskell
f1 x =  f2 (f3 x)
```

# dependencies
## 0
```haskell
f2 :: (a, b) -> a
```
## 1
```haskell
f3 :: (T1 a, T2 b) => a -> (b, a)
```
