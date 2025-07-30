import argparse
import atexit

import loguru
import typer
from kink import di

from finetune.GRPO.hivetrainer import HiveTrainer

app = typer.Typer(
    name="fine-tuning tools.",
    no_args_is_help=True,
)


def parser_register():
    """
    Register the parsers
    :return:
    """
    parser = argparse.ArgumentParser(
        description='fine-tuning tools by stupidfish(HSC-SEC).',
        epilog='''
Example:
    %(prog)s --index_folder rss-picker --system_prompt "你是一名网络安全领域的出题专家，你需要根据给你的知识库来出题，确保后者可以通过做题来完全吸收知识库里的知识，如果提供的是广告等非纯技术类的干货，那么可以不返回问题" 
    %(prog)s --exams --input_parquet_file example.parquet
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        '--index_file',
        type=str,
        default='',
        help='Input a index txt,read line by line.'
    )

    parser.add_argument(
        '--index_folder',
        type=str,
        default='',
        help="Input a folder,i'll read all the .md files."
    )

    parser.add_argument(
        '--input_parquet_file',
        type=str,
        default='',
        help='Path to the input parquet file.'
    )
    parser.add_argument(
        '--encoding',
        type=str,
        default='',
        help='file encoding with markdowns.'
    )
    parser.add_argument(
        '--instruction',
        type=str,
        default='',
        help="Alpaca's instruction for the fine-tuning process."
    )
    parser.add_argument(
        '--system_prompt',
        type=str,
        default="请根据题目和原文作答，并给出准确的答案。",
        help="System prompt for the fine-tuning process."
    )
    parser.add_argument(
        '--response_prefix',
        type=str,
        default="<think>",
        help="Prefix to be added before the response."
    )
    parser.add_argument(
        '--response_suffix',
        type=str,
        default='',
        help="Suffix to be added after the response."
    )

    parser.add_argument(
        '--exams',
        action='store_true',
        help="Execute the exam method."
    )
    parser.add_argument(
        '--exams_thread',
        type=int,
        default=20,
        help="Threads of exams."
    )

    parser.add_argument(
        '--gen_questions',
        action='store_true',
        help="Generate questions for exam."
    )

    parser.add_argument(
        '--convert_json_tmp_to_alpaca_file_path',
        type=str,
        default='',
        help="Convert json.tmp's file to alpaca json dataset."
    )

    parser.add_argument(
        '--openai_api_key',
        type=str,
        default='',
        help="OpenAI API key for accessing OpenAI services."
    )

    parser.add_argument(
        '--openai_api_endpoint',
        type=str,
        default='http://gpus.dev.cyberspike.top:8000/v1',
        help="OpenAI API endpoint for accessing OpenAI services."
    )
    parser.add_argument(
        '--default_model',
        type=str,
        default='QwQ-32B',
        help="Default model for OpenAI API."
    )
    parser.add_argument(
        '--recovery_parquet_from_pkl',
        type=str,
        default='',
        help="Recovery parquet from pkl."
    )
    parser.add_argument(
        '--convert_parquet_to_json',
        type=str,
        default='',
        help="Directly convert parquet to json."
    )
    parser.add_argument(
        '--filter_parquet_instructions',
        type=str,
        default='我要求他只能是技术类的干货，比如漏洞复现、前沿技术分析等、记录实战经历等，而不是展望未来、某某会议、广告等内容，且问题描述清晰。',
        help="筛选问题集的指令，请仿照default内容进行直接的要求"
    )

    args = parser.parse_args()
    for arg in args.__dict__:
        if arg not in di:
            di[arg] = args.__dict__[arg]

    return parser, args


from finetune.parquet.fine_tuning.tools import finetune_tools

FT = finetune_tools()
atexit.register(FT.save)  # 不用管


@app.command()
def exam():
    """
    Execute the exam method.
    """
    FT.exam()


@app.command()
def gen_questions():
    """
    Generate questions for exam.
    """
    FT.gen_questions()


@app.command()
def gen_questions_by_index_file():
    """
    Generate questions by index file.
    """
    FT.gen_questions_by_index_file()


@app.command()
def gen_questions_by_index_folder():
    """
    Generate questions by index folder.
    """
    FT.gen_questions_by_index_folder()


@app.command()
def convert_json_tmp_to_alpaca_file_path(convert_json_tmp_to_alpaca_file_path: str):
    """
    Convert json.tmp's file to alpaca json dataset.
    """
    FT.convert_json_tmp_to_alpaca(convert_json_tmp_to_alpaca_file_path)


@app.command()
def recovery_parquet_from_pkl_invoke():
    """
    Recovery parquet from pkl.
    """
    FT.recovery_parquet_from_pkl_invoke()


@app.command()
def convert_parquet_to_json_invoke():
    """
    Directly convert parquet to json.
    """
    FT.convert_parquet_to_json_invoke()


@app.command()
def filter_parquet_instructions_invoke(filter_parquet_instructions: str):
    """
    筛选问题集的指令，请仿照default内容进行直接的要求
    """
    FT.filter_parquet_instructions_invoke(filter_parquet_instructions)


@app.command()
def hive_reward_train(
        hive_reward_folder_path: str = typer.Argument(..., help="Path to the hive-reward dataset folder."),
        model_name: str = typer.Argument('Qwen2.5-0.5B-Instruct', help="Model name for training."),
        SYSTEM_PROMPT: str = typer.Argument(
            '你是一名专家，请不要直接给出答案，而是经过严谨而深思熟虑的思考后再给出答案，其中要把每一步的思考过程不可省略的详细说出来，并把思考过程放在<think></think>中显示。',
            help="System prompt for the training faster."),
        SYSTEM_PROMPT_FREQ: float = typer.Argument(0.1, help="Frequency of the system prompt in the training."),
        max_prompt_length: int = typer.Argument(25565, help="Maximum prompt length for the training."),
        max_seq_length: int = typer.Argument(128000, help="Maximum sequence length for the training."),
        alpaca_dataset_path: str = typer.Argument("", help="Path to the alpaca dataset for training."),
        logging_steps: int = typer.Argument(10, help="Logging steps for the training."),
        save_steps: int = typer.Argument(1000, help="Save steps for the training."),
        use_vllm: bool = typer.Argument(True, help="Whether to use vllm for training."),
        report_to: str = typer.Argument("tensorboard",
                                        help="Reporting tool for the training, e.g., 'wandb' or 'tensorboard'."),
        fp16: bool = typer.Argument(True, help="Whether to use fp16 for training."),
        learning_rate: float = typer.Argument(2e-4, help="Learning rate for the training."),
        num_train_epochs: int = typer.Argument(3, help="Number of training epochs."),
        max_steps: int = typer.Argument(10000, help="Maximum number of training steps."),
        train_model: list[str] = typer.Argument(['q_proj', 'k_proj', 'v_proj'],
                                                help="List of model components to train."),
        LoRA_r: int = typer.Argument(8, help="LoRA rank for the training."),
        LoRA_alpha: int = typer.Argument(16, help="LoRA alpha for the training."),
):
    T = HiveTrainer(
        **locals()  # unpack all local variables as arguments
    )
    T.train()


def main():
    """
    entrypoint
    """
    app()
