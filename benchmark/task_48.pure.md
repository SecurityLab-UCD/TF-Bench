
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--gcd

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => a -> a -> a
```   

# code
```haskell
f1 x y =  f2 (f3 x) (f3 y)
  where 
    f2 a 0  =  a
    f2 a b  =  f2 b (f4 a b)
```

# dependencies
## 0
```haskell
f3 :: T2 a => a -> a
```
## 1
```haskell
f4 :: T1 a => a -> a -> a
```
