
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--lcm

# poly_type
Ad-hoc

# signature
```haskell
lcm :: Integral a => a -> a -> a
```   

# code
```haskell
lcm 0 _ =  0
lcm _ 0 =  0
lcm x y =  abs ((x `quot` (gcd x y)) * y)
```

# dependencies
## 0
```haskell
abs :: Num a => a -> a
```
## 1
```haskell
gcd :: Integral a => a -> a -> a
```
## 2
```haskell
(*) :: Num a => a -> a -> a
```
## 3
```haskell
quot :: Integral a => a -> a -> a
```