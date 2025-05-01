
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
abs n  = if n > zero then n else negate n
```

# dependencies
## 0
```haskell
(>) :: Ord a => a -> a -> Bool
```
## 1
```haskell
negate :: Num a => a -> a
```
## 2
```haskell
zero :: Int
```

