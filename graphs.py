import numpy as np
import pandas as pd


def speed_life_data(feed, depth, tool_material, operation, workpiece_material, predictor):
    speed_vals = np.arange(60, 221, 10)
    life_vals = [
        predictor(speed, feed, depth, tool_material, operation, workpiece_material).tool_life
        for speed in speed_vals
    ]
    table = pd.DataFrame({
        "Cutting Speed": speed_vals,
        "Tool Life": np.round(life_vals, 2)
    })
    return speed_vals, life_vals, table


def feed_life_data(speed, depth, tool_material, operation, workpiece_material, predictor):
    feed_vals = np.arange(0.1, 0.51, 0.02)
    feed_life = [
        predictor(speed, feed, depth, tool_material, operation, workpiece_material).tool_life
        for feed in feed_vals
    ]
    table = pd.DataFrame({
        "Feed Rate": np.round(feed_vals, 2),
        "Tool Life": np.round(feed_life, 2)
    })
    return feed_vals, feed_life, table


def depth_life_data(speed, feed, tool_material, operation, workpiece_material, predictor):
    depth_vals = np.arange(1, 5.5, 0.5)
    depth_life = [
        predictor(speed, feed, depth, tool_material, operation, workpiece_material).tool_life
        for depth in depth_vals
    ]
    table = pd.DataFrame({
        "Depth of Cut": depth_vals,
        "Tool Life": np.round(depth_life, 2)
    })
    return depth_vals, depth_life, table


def wear_progression_data(speed, feed, depth, tool_material, operation, workpiece_material, predictor):
    predicted_life = predictor(speed, feed, depth, tool_material, operation, workpiece_material).tool_life
    time_vals = np.linspace(0, predicted_life, 9)
    wear_vals = [
        (time / max(predicted_life, 1)) * 100
        for time in time_vals
    ]
    wear_vals[-1] = 100.0
    table = pd.DataFrame({
        "Machining Time": np.round(time_vals, 2),
        "Tool Wear": np.round(wear_vals, 2)
    })
    return time_vals, wear_vals, table
