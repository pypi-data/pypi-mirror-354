import vidtoolz
import os
from vidtoolz_add_text.add_text import add_text_to_video, write_file
import sys


def determine_output_path(input_file, output_file):
    input_dir, input_filename = os.path.split(input_file)
    name, _ = os.path.splitext(input_filename)

    if output_file:
        output_dir, output_filename = os.path.split(output_file)
        if not output_dir:  # If no directory is specified, use input file's directory
            return os.path.join(input_dir, output_filename)
        return output_file
    else:
        return os.path.join(input_dir, f"{name}_text.mp4")


def create_parser(subparser):
    parser = subparser.add_parser("addtext", description="Add text to a video file")
    parser.add_argument("main_video", help="Path to the main video file.")
    parser.add_argument("-t", "--text", help="Text to write")

    parser.add_argument(
        "-mt",
        "--multi-text",
        action="append",
        help='Multi-text in format "text,start,duration". Can be used multiple times. ex "hello,1:20,10" ',
    )

    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output video file name (default: %(default)s)",
    )
    parser.add_argument(
        "-p",
        "--position",
        choices=[
            "top-left",
            "top-right",
            "bottom-left",
            "bottom-right",
            "center",
            "bottom",
        ],
        default="bottom",
        help="Position of the text (default: %(default)s)",
    )
    parser.add_argument(
        "-st",
        "--start-time",
        type=float,
        default=0,
        help="Start time when text should appear: (default: %(default)s)",
    )
    parser.add_argument(
        "-et",
        "--end-time",
        type=float,
        default=None,
        help="End time when text should disappear. (default: %(default)s)",
    )
    parser.add_argument(
        "-f", "--fontsize", type=int, default=50, help="Fontsize (default: %(default)s)"
    )

    parser.add_argument(
        "-pad", "--padding", type=int, default=50, help="Padding (default: %(default)s)"
    )

    parser.add_argument(
        "-d",
        "--duration",
        type=float,
        default=4,
        help="Duration in seconds (default: %(default)s)",
    )

    return parser


class ViztoolzPlugin:
    """Add text to a video file"""

    __name__ = "addtext"

    @vidtoolz.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        if args.text and args.multi_text:
            sys.exit("Error: Use either  --text or --multi-text, not both.")

        if args.text is None and args.multi_text is None:
            sys.exit("Error: Use either  --text or --multi-text, should be provided")

        output = determine_output_path(args.main_video, args.output)
        clip, fps = add_text_to_video(
            args.main_video,
            args.text,
            args.start_time,
            args.end_time,
            args.position,
            args.fontsize,
            args.padding,
            args.duration,
            args.multi_text,
        )
        write_file(clip, output, fps)

    def hello(self, args):
        # this routine will be called when "vidtoolz "addtext is called."
        print("Hello! This is an example ``vidtoolz`` plugin.")


addtext_plugin = ViztoolzPlugin()
