
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--isNaN-Double

# poly_type
Monomorphic

# signature
```haskell
isNaN :: Double -> Bool
```   

# code
```haskell
isNaN x = zero /= isDoubleNaN x
```

# dependencies
## 0
```haskell
isDoubleNaN :: Double -> Int
```
## 1
```haskell
(/=) :: Eq a => a -> a -> Bool
```
## 2
```haskell
zero :: Int
```