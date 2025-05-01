
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/List.hs--replicate

# poly_type
Parametric

# signature
```haskell
replicate :: Int -> a -> [a]
```   

# code
```haskell
replicate n x =  take n (repeat x)
```

# dependencies
## 0
```haskell
take :: Int -> [a] -> [a]
```
## 1
```haskell
repeat :: a -> [a]
```
