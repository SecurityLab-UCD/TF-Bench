
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--significand

# poly_type
Parametric

# signature
```haskell
f1 :: T1 a => a -> a
```   

# code
```haskell
f1 x = f2 m (f3 (f4 x))
    where (m,_) = f5 x
```

# dependencies
## 0
```haskell
f2 :: T1 a => T2 -> T3 -> a
```
## 1
```haskell
f5 :: T1 a => a -> (T2, T3)
```
## 2
```haskell
f4 :: T1 a => a -> T3
```
## 3
```haskell
f3 :: T4 a => a -> a
```