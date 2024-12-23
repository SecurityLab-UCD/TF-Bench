
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Num.hs--abs-Int

# poly_type
Monomorphic

# signature
```haskell
abs :: Int -> Int
```   

# code
```haskell
abs n  = if n > 0 then n else negate n
```

# dependencies
## 0
```haskell
(>) :: Int -> Int -> Bool
```
## 1
```haskell
negate :: Int -> Int
```
