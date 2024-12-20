
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Real.hs--divMod

# poly_type
Ad-hoc

# signature
```haskell
divMod :: Integral a => a -> a -> (a,a)
```   

# code
```haskell
divMod n d =  if signum r == negate (signum d) then (q-1, r+d) else qr
    where qr@(q,r) = quotRem n d
```

# dependencies
## 0
```haskell
quotRem :: Integral a => a -> a -> (a, a)
```
## 1
```haskell
negate :: Num a => a -> a
```
## 2
```haskell
(+) :: Num a => a -> a -> a
```
## 3
```haskell
(-) :: Num a => a -> a -> a
```
## 4
```haskell
signum :: Num a => a -> a
```
