
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--toEnum-Bool

# poly_type
Monomorphic

# signature
```haskell
toEnum :: Int -> Bool
```   

# code
```haskell
toEnum n | n == zero   = False
         | n == one    = True
         | otherwise = error "bad argument"
```

# dependencies
## 0
```haskell
data Bool = False | True
```
## 1
```haskell
(==) :: Eq a => a -> a -> Bool
```
## 2
```haskell
zero :: Int
```
## 3
```haskell
one :: Int
```
