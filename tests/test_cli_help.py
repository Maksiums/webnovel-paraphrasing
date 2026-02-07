from typer.testing import CliRunner

from webnovel_paraphraser.cli import app

runner = CliRunner()


def test_help_lists_expected_subcommands() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "inspect-epub" in result.stdout
    assert "split-epub" in result.stdout
    assert "paraphrase-chapter" in result.stdout
    assert "build-epub" in result.stdout
