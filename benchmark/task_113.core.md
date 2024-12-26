
# task_id
data/repos/ghc-internal-9.1001.0/src/GHC/Internal/Show.hs--showParen

# poly_type
Monomorphic

# signature
```haskell
showParen :: Bool -> ShowS -> ShowS
```   

# code
```haskell
showParen b p   =  if b then showChar leftParenthesis . p . showChar rightParenthesis else p
```

# dependencies
## 0
```haskell
showChar :: Char -> ShowS
```
## 1
```haskell
(.) :: (b -> c) -> (a -> b) -> a -> c
```
## 2
```haskell
leftParenthesis :: Char
```
## 3
```haskell
rightParenthesis :: Char
```
## 4
```haskell
type ShowS = String -> String
```