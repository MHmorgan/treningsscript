module Page.Session exposing (..)


import Html exposing (..)
import Html.Attributes exposing (class)
import Html.Events exposing (onClick)
import Http
import Debug
import Skeleton
import Task
import Time
import Json.Decode as D exposing (Decoder)
import Page.Session.Exercise as ExercisePage



-- MODEL


-- TODO Handle storage of state later
type alias Model =
  { day : String  -- Push, Pull, etc.
  , start : Time.Posix
  , duration : Int  -- in seconds
  , error : Maybe String
  , state : State

  -- From the server
  , exercises : List Exercise
  , warmups : List Warmup

  -- Added by the user
  , exerciseEntries : List ExerciseEntry
  , warmupEntry : Maybe WarmupEntry
  }


type State
  = Loading
  | ChooseExercise
  | AddExerciseEntry EEForm
  --| AddWarmup WEntryForm


-- Exercise Entry Form
type alias EEForm =
  { exercise : Exercise
  , reps : List Int
  , weight : Maybe Int
  , onerepmax : Maybe Int
  }


init : String -> ( Model, Cmd Msg )
init day =
  ( { default | day = day }
  , Cmd.batch
    [ Task.perform SetStart Time.now
    , Http.get
      { url = "/api/exercises"
      , expect = Http.expectJson GotExercises (D.list exerciseDecoder)
      }
    , Http.get
      { url = "/api/warmups"
      , expect = Http.expectJson GotWarmups (D.list warmupDecoder)
      }
    ]
  )


default : Model
default =
  { day = ""
  , start = Time.millisToPosix 0
  , duration = 0
  , error = Nothing
  , state = Loading
  , exercises = []
  , warmups = []
  , exerciseEntries = []
  , warmupEntry = Nothing
  }


initEEForm : Exercise -> EEForm
initEEForm exercise =
  { exercise = exercise
  , reps = []
  , weight = Nothing
  , onerepmax = Nothing
  }



-- EXERCISE


type alias Exercise =
  { name : String
  , daytype : String
  , weighttype : String
  , entries : List ExerciseEntry
  }


type alias ExerciseEntry =
  { date : String
  , reps : List Int
  , weight : Maybe Int
  , onerepmax : Maybe Int
  }


exerciseDecoder : Decoder Exercise
exerciseDecoder =
  D.map4 Exercise
    (D.field "name" D.string)
    (D.field "daytype" D.string)
    (D.field "weighttype" D.string)
    (D.field "entries" (D.list exerciseEntryDecoder))


exerciseEntryDecoder : Decoder ExerciseEntry
exerciseEntryDecoder =
  D.map4 ExerciseEntry
    (D.field "date" D.string)
    (D.field "reps" (D.list D.int))
    (D.field "weight" (D.maybe D.int))
    (D.field "onerepmax" (D.maybe D.int))



-- WARMUP


type alias Warmup =
  { name : String
  , entries : List WarmupEntry
  }


type alias WarmupEntry =
  { date : String
  , intervals : List Int
  }


warmupDecoder : Decoder Warmup
warmupDecoder =
  D.map2 Warmup
    (D.field "name" D.string)
    (D.field "entries" (D.list warmupEntryDecoder))


warmupEntryDecoder : Decoder WarmupEntry
warmupEntryDecoder =
  D.map2 WarmupEntry
    (D.field "date" D.string)
    (D.field "intervals" (D.list D.int))



-- SESSION


type alias Session =
  { day : String
  , length : Float
  , daytype : String
  }


sessionDecoder : Decoder Session
sessionDecoder =
  D.map3 Session
    (D.field "day" D.string)
    (D.field "length" D.float)
    (D.field "daytype" D.string)



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
  Time.every 1000 UpdateDuration



-- UPDATE


type Msg
  = None
  | SetStart Time.Posix
  | UpdateDuration Time.Posix
  | GotExercises (Result Http.Error (List Exercise))
  | GotWarmups (Result Http.Error (List Warmup))
  | AddExerciseEntry Exercise


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    None ->
      ( model, Cmd.none )

    SetStart start ->
      ( { model | start = start } , Cmd.none )

    UpdateDuration now ->
      let
        duration =
          ( Time.posixToMillis now - Time.posixToMillis model.start ) // 1000
      in
      ( { model | duration = duration } , Cmd.none )

    GotExercises (Ok exercises) ->
      let
        state = if List.isEmpty model.warmups then Loading else ChooseExercise
      in
      ( { model | exercises = exercises, state = state } , Cmd.none )

    GotExercises (Err error) ->
        ( { model | error = Just ("Error " ++ Debug.toString error) }, Cmd.none )

    GotWarmups (Ok warmups) ->
      let
        state = if List.isEmpty model.exercises then Loading else ChooseExercise
      in
      ( { model | warmups = warmups, state = state } , Cmd.none )

    GotWarmups (Err error) ->
        ( { model | error = Just ("Error " ++ Debug.toString error) }, Cmd.none )

    AddExerciseEntry exercise ->
      let
        state = AddExerciseEntry (ExercisePage.init exercise)
      in
      ( { model | state = state } , Cmd.none )



-- VIEW


view : Model -> Skeleton.Details Msg
view model =
  case model.state of
    Loading ->
      { title = "Session"
      , header = "Loading Session"
      , attrs = []
      , kids = [ text "Loading..." ]
      }

    ChooseExercise ->
      { title = "Training Session"
      , header = (model.day ++ " - " ++ viewDuration model.duration)
      , attrs = []
      , kids = viewChooseExercise model
      }

    _ ->
      { title = "Training Session"
      , header = (model.day ++ " - " ++ viewDuration model.duration)
      , attrs = []
      , kids =
        [ p [] [ text ("Day: " ++ Debug.toString model.day) ]
        , p [] [ text ("Exercises: " ++ Debug.toString model.exercises) ]
        , p [] [ text ("Warmup: " ++ Debug.toString model.warmups) ]
        ]
      }



-- VIEW LOADING


viewLoading : List (Html Msg)
viewLoading =
  [ p [] [ text "Loading..." ]
  ]



-- VIEW CHOOSE EXERCISE


viewChooseExercise : Model -> List (Html Msg)
viewChooseExercise model =
  let
    exercises =
      List.map chooseExercise
        (List.filter (\e -> e.daytype == model.day) model.exercises)
  in
  exercises


chooseExercise : Exercise -> Html Msg
chooseExercise exercise =
  let
    name = String.toUpper exercise.name
    wt = exercise.weighttype
  in
  div [ class "container" ]
    [ span [ class "fs-4" ] [ text name ]
    , button [ class "btn btn-primary", onClick (AddExerciseEntry exercise) ]
      [ text "+" ]
    ]


-- UTILS


viewDuration : Int -> String
viewDuration duration =
  let
    seconds =
      String.fromInt (modBy 60 duration)

    minutes =
      String.fromInt (modBy 60 (duration // 60))

    hours =
      duration // 3600
  in
    if hours > 0 then
      String.fromInt hours ++ ":" ++ minutes ++ ":" ++ seconds

    else
      minutes ++ ":" ++ seconds

