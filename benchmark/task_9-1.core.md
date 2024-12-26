
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Enum.hs--fromEnum-Bool

# poly_type
Monomorphic

# signature
```haskell
fromEnum :: Bool -> Int
```

# note
modified

# code
```haskell
fromEnum False = zero
fromEnum True  = one
```

# dependencies
## 0
```haskell
data Bool = False | True
```
## 1
```haskell
zero :: Int
```
## 2
```haskell
one :: Int
```