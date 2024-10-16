from manim import *

class ScaleTriangle(Scene):
    def construct(self):
        # Create x and y axes
        axes = Axes(
            x_range=[-10, 10, 1], y_range=[-10, 10, 1],
            axis_config={"color": BLUE}
        )
        self.play(Create(axes))

        # Define the initial triangle points
        original_coords = [[1, 1], [3, 1], [2, 3]]
        triangle_points = [axes.coords_to_point(*coord) for coord in original_coords]

        # Create the triangle
        triangle = Polygon(*triangle_points, color=YELLOW)
        self.play(Create(triangle), run_time=3)

        # Label the initial triangle vertices
        vertex_labels = [
            MathTex(f"({x}, {y})")
            .next_to(axes.coords_to_point(x, y), UP, buff=0.4)
            .scale(0.6)
            for x, y in original_coords
        ]
        self.play(*[Write(label) for label in vertex_labels], run_time=2)

        self.wait(1)

        # Display the scaling matrix
        scaling_matrix = [[2, 0], [0, 2]]
        matrix = MathTex(r"2 \cdot \left[ \begin{array}{cc} 1 & 0 \\ 0 & 1 \end{array} \right]")
        matrix.to_corner(UP + LEFT)
        self.play(Write(matrix))

        # Variables to store the previous column matrix and equals sign for fading out
        previous_vector = None
        previous_equals = None
        final_dots = []

        # Animate the multiplication process for each vertex
        for i, (coord, label) in enumerate(zip(original_coords, vertex_labels)):
            # If there was a previous column matrix and equals sign, fade them out
            if previous_vector and previous_equals:
                self.play(FadeOut(previous_vector), FadeOut(previous_equals))

            # Move the vertex label to the matrix position
            self.play(label.animate.move_to(matrix.get_right() + RIGHT), run_time=1)

            # Transform the label into a column matrix for the vertex
            vector = MathTex(rf"\left[ \begin{{array}}{{c}} {coord[0]} \\ {coord[1]} \end{{array}} \right]")
            vector.move_to(label.get_center())  # Make sure it replaces the label exactly
            self.play(Transform(label, vector))

            # Show the equals sign and result matrix
            equals = MathTex("=")
            equals.next_to(vector, RIGHT)
            result = MathTex(
                rf"\left[ \begin{{array}}{{c}} {coord[0] * scaling_matrix[0][0]} \\ {coord[1] * scaling_matrix[1][1]} \end{{array}} \right]"
            )
            result.next_to(equals, RIGHT)

            self.play(Write(equals), Write(result))
            self.wait(0.5)

            # Move the result matrix to the transformed point in the xy-plane
            transformed_coord = [coord[0] * scaling_matrix[0][0], coord[1] * scaling_matrix[1][1]]
            transformed_point = axes.coords_to_point(*transformed_coord)
            self.play(result.animate.move_to(transformed_point), run_time=1)

            # Turn the result matrix into a dot at the transformed position
            dot = Dot(point=transformed_point, color=RED)
            self.play(Transform(result, dot), run_time=0.5)
            final_dots.append(dot)  # Store the final dots

            # Store the transformed label (now a column matrix) and equals sign for fading out in the next iteration
            previous_vector = label  # The label has become the matrix at this point
            previous_equals = equals

        # Fade out the last column matrix before transforming the triangle
        self.play(FadeOut(previous_vector), FadeOut(previous_equals))

        # Apply the scaling transformation to the triangle
        scaled_triangle = triangle.copy().apply_matrix(scaling_matrix)

        # Animate the triangle scaling
        self.play(triangle.animate.apply_matrix(scaling_matrix), run_time=2)

        # Fill the transformed triangle with a color
        new_coords = [[2 * x, 2 * y] for x, y in original_coords]
        filled_triangle = Polygon(*[axes.coords_to_point(*coord) for coord in new_coords], color=GREEN, fill_opacity=0.5)
        self.play(Transform(scaled_triangle, filled_triangle))

        # Label the final vertices of the transformed triangle
        final_vertex_labels = [
            MathTex(f"({x}, {y})")
            .next_to(filled_triangle.get_vertices()[i], UP, buff=0.4)
            .scale(0.6)
            for i, (x, y) in enumerate(new_coords)
        ]
        self.play(*[Write(label) for label in final_vertex_labels], run_time=2)

        # Keep the final image on the screen for a moment
        self.wait(2)
