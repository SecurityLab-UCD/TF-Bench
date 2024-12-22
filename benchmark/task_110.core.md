
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Show.hs--showsPrec

# poly_type
Adhoc

# signature
```haskell
showsPrec :: Show a => Int -> a -> ShowS
```   

# code
```haskell
showsPrec _ x s = show x ++ s
```

# dependencies
## 0
```haskell
show ::Show a => a -> String
```
## 1
```haskell
(++) :: [a] -> [a] -> [a]
```
## 4
```haskell
type ShowS = String -> String
```