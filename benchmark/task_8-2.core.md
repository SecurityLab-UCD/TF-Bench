
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--toEnum-Ordering

# poly_type
Monomorphic

# signature
```haskell
toEnum :: Int -> Ordering
```   

# code
```haskell
toEnum n | n == zero = LT
         | n == one  = EQ
         | n == two  = GT
         | otherwise = error "bad argument"
```

# dependencies
## 0
```haskell
data Ordering = LT | EQ | GT
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
## 4
```haskell
two :: Int
```