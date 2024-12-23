
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Data/OldList.hs--unwords

# poly_type
Monomorphic

# signature
```haskell
unwords :: [String] -> String
```   

# code
```haskell
unwords [] =  ""
unwords ws =  foldr1 (\w s -> w ++ ' ':s) ws
```

# dependencies
## 0
```haskell
(++) :: [a] -> [a] -> [a]
```
## 1
```haskell
foldr1 :: (a -> a -> a) -> t a -> a
```
## 2
```haskell
(:) :: a -> [a] -> [a]
```
## 3
```haskell
[] :: [a]
```
## 4
```haskell
' ' :: Char
```