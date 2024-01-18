mes:
        scaled_frame = frame.resize((SCALE_SIZE, SCALE_SIZE), Image.Resampling.NEAREST)

        print(f"Frame format: {frame.format}, size: {frame.size}")

        # Display the scaled-up image
        display_image(frame, window, (0, 0))
        display_image(scaled_frame, window, (MIRROR_WIDTH, 0))

        time.sleep(TOP_FRAME