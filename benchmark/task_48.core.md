
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--gcd

# poly_type
Ad-hoc

# signature
```haskell
gcd :: Integral a => a -> a -> a
```   

# code
```haskell
gcd x y =  gcd' (abs x) (abs y)
  where 
    gcd' a 0  =  a
    gcd' a b  =  gcd' b (a `rem` b)
```

# dependencies
## 0
```haskell
abs :: Num a => a -> a
```
## 1
```haskell
rem :: Integral a => a -> a -> a
```
