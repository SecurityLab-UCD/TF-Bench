
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Show.hs--showList

# poly_type
Ad-hoc

# signature
```haskell
showList :: Show a => [a] -> ShowS
```   

# code
```haskell
showList ls   s = showList__ shows ls s
```

# dependencies
## 0
```haskell
showList__ :: (a -> ShowS) -> [a] -> ShowS
```
## 1
```haskell
shows :: Show a => a -> ShowS
```
## 2
```haskell
type ShowS = String -> String
```
