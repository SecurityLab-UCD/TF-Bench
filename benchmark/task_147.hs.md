
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Float.hs--tan

# poly_type
Ad-hoc

# signature
```haskell
tan :: Floating a => a -> a
```   

# code
```haskell
tan x = sin x / cos x
```

# dependencies
## 0
```haskell
sin :: Floating a => a -> a
```
## 1
```haskell
cos :: Floating a => a -> a
```
## 2
```haskell
(/) :: Fractional a => a -> a -> a
```
