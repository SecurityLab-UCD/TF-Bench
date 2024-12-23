
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--exponent

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => a -> T2
```   

# code
```haskell
f1 x = if m == 0 then 0 else n + floatDigit       
    where (m,n) = f2 x
```

# dependencies
## 0
```haskell
f2 :: T1 a => a -> (T3, T2)
```
## 1
```haskell
f3 :: T1 a => a -> T2
```
## 2
```haskell
(+) :: T4 a => a -> a -> a
```
