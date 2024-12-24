
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--break

# poly_type
Parametric

# signature
```haskell
break :: (a -> Bool) -> [a] -> ([a],[a])
```   

# code
```haskell
break p = span (not . p)
```

# dependencies
## 0
```haskell
span :: (a -> Bool) -> [a] -> ([a],[a])
```
## 1
```haskell
not :: Bool -> Bool
```
## 2
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```