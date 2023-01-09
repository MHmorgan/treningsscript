module Common exposing (..)

import Html exposing (Html, div, h1, main_, node, text)
import Html.Attributes exposing (attribute, class, href, property, rel)
import Json.Encode as Encode


page : String -> List (Html a) -> Html a
page title elems =
  div [ ] (
    -- Viewport meta tag
    [ node "meta"
      [ property "name" (Encode.string "viewport")
      , property "content" (Encode.string "width=device-width, initial-scale=1")
      ] []

    -- Bootstrap CSS
    , node "link"
      [ rel  "stylesheet"
      , href "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css"
      ] []

    , div [ ] (
      [ div [ class "container-fluid py-3" ]
        [ div [ class "container" ]
          [ h1
            [ class "display-1" ]
            [ text title ]
          ]
        ]
      ] ++ elems)
    ])
