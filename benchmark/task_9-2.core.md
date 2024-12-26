
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--fromEnum-Ordering

# poly_type
Monomorphic

# signature
```haskell
fromEnum :: Ordering -> Int
```   

# code
```haskell
fromEnum LT = zero
fromEnum EQ = one
fromEnum GT = two
```

# dependencies
## 0
```haskell
data Ordering = LT | EQ | GT
```
## 1
```haskell
zero :: Int
```
## 2
```haskell
one :: Int
```
## 3
```haskell
two :: Int
```
