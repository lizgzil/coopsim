from argparse import ArgumentParser

from coopsim.prisoners_dilemma import PrisonersDilemma
from coopsim.visualise import save_animation

game_configs = {
    0: {
        'description': 'Fig 3 of Nowak and May - Symmetrical snowflakes',
        'payoffs': {'t': 1.9, 'r': 1, 'p': 0, 's': 0},
        'init_coop' : None,
        'special_init': True
        },
    1: {
        'description': 'Fig 1a of Nowak and May - Static strings',
        'payoffs': {'t': 1.79, 'r': 1, 'p': 0, 's': 0},
        'init_coop' : 0.5,
        'special_init': False
        },
    2: {
        'description': 'Fig 1b of Nowak and May - Spatial chaos',
        'payoffs': {'t': 1.9, 'r': 1, 'p': 0, 's': 0},
        'init_coop' : 0.5,
        'special_init': False
        }
}

def create_argparser():

    parser = ArgumentParser()

    parser.add_argument(
        '--game_config_num',
        default=0,
        type=int
    )
    parser.add_argument(
        '--grid_len',
        default=100,
        type=int
    )
    parser.add_argument(
        '--num_iterations',
        default=100,
        type=int
    )

    return parser


if __name__ == '__main__':    

    parser = create_argparser()
    args = parser.parse_args()

    game_config_num = args.game_config_num

    grid_len = args.grid_len
    num_iterations = args.num_iterations
    plot_size_n = 5 # Size of video

    payoffs = game_configs[game_config_num]['payoffs']
    init_coop = game_configs[game_config_num]['init_coop']
    special_init = game_configs[game_config_num]['special_init']

    prd = PrisonersDilemma(payoffs, grid_len, init_coop, num_iterations, special_init)

    strategies_all, changes_all = prd.run_simulation()

    videoname = "videos/game{}_{}its_size{}x{}.mp4".format(game_config_num, num_iterations, grid_len, grid_len)
    save_animation(changes_all, videoname, plot_size_n=plot_size_n)

