
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Num.hs--signum-Int

# poly_type
Monomorphic

# signature
```haskell
signum :: Int -> Int
```   

# code
```haskell
signum n | n `ltInt` 0 = negate 1
         | n `eqInt` 0 = 0
         | otherwise   = 1
```

# dependencies
## 0
```haskell
negate :: Int -> Int
```
## 1
```haskell
ltInt :: Int -> Int -> Bool
```
## 2
```haskell
eqInt :: Int -> Int -> Bool
```
