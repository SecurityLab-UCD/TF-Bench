
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--tanh

# poly_type
Ad-hoc

# signature
```haskell
tanh :: Floating a => a -> a
```   

# code
```haskell
tanh x = sinh x / cosh x
```

# dependencies
## 0
```haskell
sinh :: Floating a => a -> a
```
## 1
```haskell
cosh :: Floating a => a -> a
```
## 2
```haskell
(/) :: Fractional a => a -> a -> a
```