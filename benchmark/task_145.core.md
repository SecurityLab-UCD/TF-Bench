
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--(**)

# poly_type
Ad-hoc

# signature
```haskell
(**) :: Floating a => a -> a -> a
```   

# code
```haskell
x ** y = exp (log x * y)
```

# dependencies
## 0
```haskell
exp :: Floating a => a -> a
```
## 1
```haskell
log :: Floating a => a -> a
```
## 2
```haskell
(*) :: Num a => a -> a -> a
```

