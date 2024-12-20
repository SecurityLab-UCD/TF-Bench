
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--fromRational

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => T2 -> a
```   

# code
```haskell
f1 (x:%y) = f2 x % f2 y
```

# dependencies
## 0
```haskell
f2 :: T3 a => T4 -> a
```
## 1
```haskell
(%) :: (T5 a) => a -> a -> Ratio a
```
## 2
```haskell
(:%) :: T4 -> T4 -> T2
```
