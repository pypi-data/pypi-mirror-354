<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { BlockTitle } from "@gradio/atoms";
	import { Block } from "@gradio/atoms";
	import { StatusTracker, type LoadingStatus } from "@gradio/statustracker";
	import { Chess } from "chess.js";
	import type { ChessBoardInstance } from "chessboardjs";
	import { BaseCheckbox } from "@gradio/checkbox";
	import { BaseTextbox } from "@gradio/textbox";
	import { BaseButton } from "@gradio/button";
	import { BaseRadio } from "@gradio/radio";
	import Row from "@gradio/row";
	import Column from "@gradio/column";

	export let gradio: Gradio<{
		change: never;
		submit: never;
		move: never;
		clear_status: LoadingStatus;
	}>;
	export let label = "Chessboard";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = new Chess().fen();
	export let show_label: boolean;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let interactive: boolean;
	export let game_mode = false;
	export let orientation: "white" | "black" = "white";
	export let root: string;
	let selected: string = game_mode ? "game" : "edit";
	let game = new Chess(value);
	let board: ChessBoardInstance;
	let board_id = "board_" + Math.random().toString(36).substring(2, 15);
	let sideToMove = "White to move";
	let whiteKingside = true;
	let whiteQueenside = true;
	let blackKingside = true;
	let blackQueenside = true;
	let items = [
		{ label: "White to move", value: "White to move" },
		{ label: "Black to move", value: "Black to move" },
	];

	const initBoard = () => {
		if (game_mode) {
			board = Chessboard(board_id, {
				draggable: interactive,
				position: game.fen(),
				orientation,
				pieceTheme:
					"https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png",
				onDrop: onDrop,
				onDragStart: onDragStart,
			});
		} else {
			board = Chessboard(board_id, {
				draggable: interactive,
				position: game.fen(),
				orientation,
				pieceTheme:
					"https://chessboardjs.com/img/chesspieces/wikipedia/{piece}.png",
				sparePieces: true,
				dropOffBoard: "trash",
				onChange: onChange,
			});
		}
	};

	function resetBoard(): void {
		game.reset();
		board.start();
		value = game.fen();
		sideToMove = "White to move";
		whiteKingside = true;
		whiteQueenside = true;
		blackKingside = true;
		blackQueenside = true;
	}

	function clearBoard(): void {
		game.clear();
		board.clear();
		value = game.fen();
		sideToMove = "White to move";
		whiteKingside = false;
		whiteQueenside = false;
		blackKingside = false;
		blackQueenside = false;
	}

	function handleModeChange(mode: string | number) {
		selected = String(mode);
		game_mode = selected === "game";
		initBoard();
	}

	function handleFenChange(): void {
		if (value === null || value === "") {
			value = new Chess().fen();
		}

		if (board === undefined) {
			return;
		}

		board.position(value);
		game.load(value, { skipValidation: true });

		gradio.dispatch("change");
	}

	function onDragStart(
		source: any,
		piece: string,
		position: any,
		orientation: any,
	) {
		if (game.isGameOver()) return false;

		if (
			(game.turn() === "w" && piece.search(/^b/) !== -1) ||
			(game.turn() === "b" && piece.search(/^w/) !== -1)
		) {
			return false;
		}
	}

	function onDrop(source: any, target: any) {
		try {
			var move = game.move({
				from: source,
				to: target,
				promotion: "q", // NOTE: always promote to a queen for now
			});
		} catch (error) {
			return "snapback";
		}

		if (move === null) return "snapback";

		value = game.fen();

		gradio.dispatch("move");
	}

	function onChange(oldPos: any, newPos: any) {
		const fen = Chessboard.objToFen(newPos);
		value = generateFen(fen);
	}

	function updateValue(event: any) {
		value = generateFen(board.fen());
	}

	function generateFen(position: any): string {
		let turn = sideToMove === "White to move" ? "w" : "b";
		let castlingRights = "";
		if (whiteKingside) castlingRights += "K";
		if (whiteQueenside) castlingRights += "Q";
		if (blackKingside) castlingRights += "k";
		if (blackQueenside) castlingRights += "q";
		if (castlingRights === "") castlingRights = "-";
		return `${position} ${turn} ${castlingRights} - 0 1`;
	}

	$: if (value === null) value = new Chess().fen();
	$: value, handleFenChange();
</script>

<svelte:head>
	<script
		src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"
		defer
	></script>
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.css"
	/>
	<link
		rel="stylesheet"
		href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
	/>
	<script
		src="https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.js"
		defer
		on:load={initBoard}
	></script>
	<style>
		[class*="spare-pieces"] {
			display: flex !important;
			flex-direction: row !important;
			justify-content: center !important;
		}
	</style>
</svelte:head>

<Block {visible} {elem_id} {elem_classes} {scale} {min_width}>
	{#if !game_mode && loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
			on:clear_status={() =>
				gradio.dispatch("clear_status", loading_status)}
		/>
	{/if}
	<div class="main-container">
		<BlockTitle {root} {show_label} info={undefined}>{label}</BlockTitle>
		<div class="mode-selector">
			<BaseRadio
				display_value="Play mode"
				internal_value="game"
				{selected}
				on:input={(e) => handleModeChange(e.detail)}
			/>
			<BaseRadio
				display_value="Edit mode"
				internal_value="edit"
				{selected}
				on:input={(e) => handleModeChange(e.detail)}
			/>
		</div>
		<div class="board-container">
			<div id={board_id} style="width: 500px;"></div>
		</div>

		{#if !game_mode}
			<div class="controls-container">
				<Row style="align-items: center; gap: 2rem;">
					<!-- Side‐to‐move dropdown -->
					<Column style="flex: 0 0 50%" min_width={200}>
						<div class="dropdown-container">
							<select
								bind:value={sideToMove}
								on:change={updateValue}
							>
								{#each items as item}
									<option value={item.value}
										>{item.label}</option
									>
								{/each}
							</select>
						</div>
					</Column>

					<!-- Buttons -->
					<Column style="flex: 1">
						<BaseButton
							label="Flip"
							interactive={true}
							on:click={() => {
								board.flip();
								orientation = board.orientation()
							}}
						>
							<i class="fa-solid fa-arrows-rotate"></i>
						</BaseButton>
					</Column>
					<Column style="flex: 1">
						<BaseButton
							label="Reset"
							interactive={true}
							on:click={resetBoard}
							><i class="fa-solid fa-rotate-left"></i>
						</BaseButton>
					</Column>
					<Column style="flex: 1">
						<BaseButton
							label="Clear"
							interactive={true}
							on:click={clearBoard}
						>
							<i class="fa-solid fa-trash"></i>
						</BaseButton>
					</Column>
				</Row>

				<!-- Castling checkboxes -->
				<Row style="align-items: center; gap: 2rem;">
					<Column class="checkbox‐group" style="flex: 0 0 120px">
						<label class="header" for="white-checkbox-group"
							>White</label
						>
						<div id="white-checkbox-group">
							<BaseCheckbox
								label="(O‐O)"
								interactive={true}
								bind:value={whiteKingside}
								on:change={updateValue}
							/>
							<BaseCheckbox
								label="(O‐O‐O)"
								interactive={true}
								bind:value={whiteQueenside}
								on:change={updateValue}
							/>
						</div>
					</Column>

					<Column class="checkbox‐group" style="flex: 0 0 120px">
						<label class="header" for="black-checkbox-group"
							>Black</label
						>
						<div id="black-checkbox-group">
							<BaseCheckbox
								label="(O‐O)"
								interactive={true}
								bind:value={blackKingside}
								on:change={updateValue}
							/>
							<BaseCheckbox
								label="(O‐O‐O)"
								interactive={true}
								bind:value={blackQueenside}
								on:change={updateValue}
							/>
						</div>
					</Column>
				</Row>
				<Row class="bottom‐row">
					<Column style="flex: 1">
						<BaseTextbox label={""} bind:value />
					</Column>
				</Row>
			</div>
		{/if}
	</div>
</Block>

<style>
	.main-container {
		display: flex;
		flex-direction: column;
		width: 100%;
		justify-content: center;
		align-items: center;
		text-align: center;
	}

	  .mode-selector {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

	.board-container {
		margin-top: 2rem;
		margin-bottom: 2rem;
	}

	.header {
		font-weight: bold;
		text-align: left;
	}

	.dropdown-container {
		display: inline-block;
		width: 100%;
		position: relative;
		font-family: var(--font-sans, sans-serif);
	}

	select {
		/* Use input background fill from Gradio theme */
		background-color: var(--input-background-fill);
		/* If in dark mode, the browser picks up --input-background-fill-dark automatically */
		color: var(--input-text-color);
		/* Fallback border color */
		border: 1px solid var(--input-border-color);
		border-radius: 4px;
		padding: 0.5rem 1rem;
		width: 100%;
		appearance: none;
		-webkit-appearance: none;
		-moz-appearance: none;
		font-size: 1rem;
		cursor: pointer;
		transition:
			background-color 0.2s,
			color 0.2s,
			border-color 0.2s;
	}

	.dropdown-container::after {
		content: "▾";
		position: absolute;
		right: 1rem;
		top: 50%;
		transform: translateY(-50%);
		pointer-events: none;
		color: var(--input-text-color);
	}

	select:focus {
		outline: 2px solid
			var(--input-focus-outline-color, var(--primary-color, #ff6a00));
		outline-offset: 1px;
	}

	.controls-container {
		width: 500px;
		margin: 0 auto;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}
</style>
