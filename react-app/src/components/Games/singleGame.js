import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import React from "react";
import { NavLink, useParams } from "react-router-dom";
import { getAllGames, getOneGame } from "../../store/games";

const GetOneGame = () => {
    const dispatch = useDispatch();
    const { game_id } = useParams();

    const game = useSelector(state => state.games.allGames[game_id])
    console.log(game)

    useEffect(() => {
        dispatch(getOneGame(game_id))
        dispatch(getAllGames())
    }, [dispatch])


    if (!game) return null;

    return (
        <div>
            <h1>one game</h1>
            <div>
                {game.game_name}
            </div>



            <div>


                <div>
                    <h2>Reviews</h2>
                </div>
                <div>
                    <label>Leave a Review</label>
                    <textarea
                        type="textbox"
                    />
                </div>


            </div>
        </div>
    )
}

export default GetOneGame
