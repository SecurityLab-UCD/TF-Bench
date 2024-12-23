
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--ceiling

# poly_type
Ad-hoc

# signature
```haskell
f1 :: (T1 a, T2 b) => a -> b
```   

# code
```haskell
f1 x           =  if r > 0 then n + 1 else n
                           where (n,r) = f2 x
```

# dependencies
## 0
```haskell
f2 :: (T1 a, T2 b) => a -> (b, a)
```
## 1
```haskell
(+) :: T3 a -> a -> a
```
## 2
```haskell
(>) :: T4 a -> a -> T5
```

