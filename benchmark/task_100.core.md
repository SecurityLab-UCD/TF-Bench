
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/Foldable.hs--notElem

# poly_type
Ad-hoc

# signature
```haskell
notElem :: (Foldable t, Eq a) => a -> t a -> Bool
```   

# code
```haskell
notElem x = not . elem x
```

# dependencies
## 0
```haskell
elem :: (Foldable t, Eq a) => a -> t a -> Bool
```
## 1
```haskell
not :: Bool -> Bool
```
## 2
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
