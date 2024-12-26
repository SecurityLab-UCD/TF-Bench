
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/OldList.hs--lines

# poly_type
Monomorphic

# signature
```haskell
lines :: String -> [String]
```   

# code
```haskell
lines emptyStr =  []
lines s  =  cons (case break (== newLine) s of
       (l, s') -> (l, case s' of
                       []      -> []
                       _:s''   -> lines s''))
  where
    cons ~(h, t) =  h : t
```

# dependencies
## 0
```haskell
break :: (a -> Bool) -> [a] -> ([a],[a])
```
## 1
```haskell
(:) :: a -> [a] -> [a]
```
## 2
```haskell
[] :: [a]
```
## 3
```haskell
emptyStr :: String
```
## 4
```haskell
newLine :: Char
```
## 5
```haskell
(==) :: Eq a => a -> a -> Bool
```
