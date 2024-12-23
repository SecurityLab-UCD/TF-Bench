
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--divMod

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => a -> a -> (a,a)
```   

# code
```haskell
f1 n d =  if f2 r == f3 (f2 d) then (q-1, r+d) else qr
    where qr@(q,r) = f4 n d
```

# dependencies
## 0
```haskell
f4 :: T1 a => a -> a -> (a, a)
```
## 1
```haskell
f3 :: T2 a => a -> a
```
## 2
```haskell
(+) :: T2 a => a -> a -> a
```
## 3
```haskell
(-) :: T2 a => a -> a -> a
```
## 4
```haskell
f2 :: T2 a => a -> a
```
