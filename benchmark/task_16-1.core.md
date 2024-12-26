
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
signum n | n `ltInt` zero = negate one
         | n `eqInt` zero = zero
         | otherwise      = one
```

# dependencies
## 0
```haskell
negate :: Num a => a -> a
```
## 1
```haskell
ltInt :: Int -> Int -> Bool
```
## 2
```haskell
eqInt :: Int -> Int -> Bool
```
## 3
```haskell
zero :: Int
```
## 4
```haskell
one :: Int
```