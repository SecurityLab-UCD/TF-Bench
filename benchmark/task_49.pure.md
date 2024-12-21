
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--lcm

# poly_type
Ad-hoc

# signature
```haskell
f1 :: T1 a => a -> a -> a
```   

# code
```haskell
f1 0 _ =  0
f1 _ 0 =  0
f1 x y =  f2 ((f3 x (f4 x y)) * y)
```

# dependencies
## 0
```haskell
f2 :: T2 a => a -> a
```
## 1
```haskell
f4 :: T1 a => a -> a -> a
```
## 2
```haskell
(*) :: Num a => a -> a -> a
```
## 3
```haskell
f3 :: T1 a => a -> a -> a
```