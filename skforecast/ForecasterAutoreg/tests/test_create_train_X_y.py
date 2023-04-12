# Unit test create_train_X_y ForecasterAutoreg
# ==============================================================================
import re
import pytest
import numpy as np
import pandas as pd
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from skforecast.exceptions import MissingValuesExogWarning
from sklearn.linear_model import LinearRegression
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_None():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is None.
    """
    y = pd.Series(np.arange(10))
    exog = None
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0.],
                            [5., 4., 3., 2., 1.],
                            [6., 5., 4., 3., 2.],
                            [7., 6., 5., 4., 3.],
                            [8., 7., 6., 5., 4.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
        ),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )     

    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_series_of_float():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas series of floats.
    """
    y = pd.Series(np.arange(10))
    exog = pd.Series(np.arange(100, 110), name='exog', dtype=float)
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0., 105.],
                            [5., 4., 3., 2., 1., 106.],
                            [6., 5., 4., 3., 2., 107.],
                            [7., 6., 5., 4., 3., 108.],
                            [8., 7., 6., 5., 4., 109.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'exog']
        ),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )       

    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_dataframe_of_float():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas dataframe with two columns of floats.
    """
    y = pd.Series(np.arange(10))
    exog = pd.DataFrame({
                'exog_1' : np.arange(100, 110, dtype=float),
                'exog_2' : np.arange(1000, 1010, dtype=float)
           })
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)        
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0., 105., 1005.],
                                [5., 4., 3., 2., 1., 106., 1006.],
                                [6., 5., 4., 3., 2., 107., 1007.],
                                [7., 6., 5., 4., 3., 108., 1008.],
                                [8., 7., 6., 5., 4., 109., 1009.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'exog_1', 'exog_2']
        ),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )        
    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_series_of_int():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas series of ints.
    """
    y = pd.Series(np.arange(10))
    exog = pd.Series(np.arange(100, 110), name='exog', dtype=int)
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0., 105.],
                            [5., 4., 3., 2., 1., 106.],
                            [6., 5., 4., 3., 2., 107.],
                            [7., 6., 5., 4., 3., 108.],
                            [8., 7., 6., 5., 4., 109.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'exog']
        ).astype({'exog': int}),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )       
    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_dataframe_of_int():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas dataframe with two columns of ints.
    """
    y = pd.Series(np.arange(10))
    exog = pd.DataFrame({
                'exog_1' : np.arange(100, 110, dtype=int),
                'exog_2' : np.arange(1000, 1010, dtype=int)
           })
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)        
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0., 105., 1005.],
                                [5., 4., 3., 2., 1., 106., 1006.],
                                [6., 5., 4., 3., 2., 107., 1007.],
                                [7., 6., 5., 4., 3., 108., 1008.],
                                [8., 7., 6., 5., 4., 109., 1009.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'exog_1', 'exog_2']
        ).astype({'exog_1': int, 'exog_2': int}),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )          

    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_series_of_bool():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas series of bool.
    """
    y = pd.Series(np.arange(10))
    exog = pd.Series([True]*10, name='exog', dtype=bool)
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0., 1],
                            [5., 4., 3., 2., 1., 1],
                            [6., 5., 4., 3., 2., 1],
                            [7., 6., 5., 4., 3., 1],
                            [8., 7., 6., 5., 4., 1]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'exog']
        ).astype({'exog': bool}),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )       
    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_dataframe_of_bool():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas dataframe with two columns of bool.
    """
    y = pd.Series(np.arange(10))
    exog = pd.DataFrame({
                'exog_1' : [True]*10,
                'exog_2' : [False]*10,
           })
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)        
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0., 1, 0],
                                [5., 4., 3., 2., 1., 1, 0],
                                [6., 5., 4., 3., 2., 1, 0],
                                [7., 6., 5., 4., 3., 1, 0],
                                [8., 7., 6., 5., 4., 1, 0]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'exog_1', 'exog_2']
        ).astype({'exog_1': bool, 'exog_2': bool}),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )          

    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_series_of_str():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas series of str.
    """
    y = pd.Series(np.arange(10))
    exog = pd.Series(['string']*10, name='exog', dtype=str)
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0.],
                            [5., 4., 3., 2., 1.],
                            [6., 5., 4., 3., 2.],
                            [7., 6., 5., 4., 3.],
                            [8., 7., 6., 5., 4.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
        ).assign(exog=['string']*5),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )       
    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_dataframe_of_str():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas dataframe with two columns of str.
    """
    y = pd.Series(np.arange(10))
    exog = pd.DataFrame({
                'exog_1' : ['string']*10,
                'exog_2' : ['string']*10,
           })
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)        
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0.],
                            [5., 4., 3., 2., 1.],
                            [6., 5., 4., 3., 2.],
                            [7., 6., 5., 4., 3.],
                            [8., 7., 6., 5., 4.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
        ).assign(exog_1=['string']*5, exog_2=['string']*5),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )          

    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_series_of_category():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas series of category.
    """
    y = pd.Series(np.arange(10))
    exog = pd.Series(pd.Categorical(range(10), categories=range(10)), name='exog')
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0.],
                            [5., 4., 3., 2., 1.],
                            [6., 5., 4., 3., 2.],
                            [7., 6., 5., 4., 3.],
                            [8., 7., 6., 5., 4.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
        ).assign(exog=pd.Categorical(range(5, 10), categories=range(10))),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )       
    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_exog_is_dataframe_of_category():
    """
    Test the output of create_train_X_y when y=pd.Series(np.arange(10)) and 
    exog is a pandas dataframe with two columns of category.
    """
    y = pd.Series(np.arange(10))
    exog = pd.DataFrame({
                'exog_1' : pd.Categorical(range(10)),
                'exog_2' : pd.Categorical(range(100, 110)),
           })
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    results = forecaster.create_train_X_y(y=y, exog=exog)        
    expected = (
        pd.DataFrame(
            data = np.array([[4., 3., 2., 1., 0.],
                            [5., 4., 3., 2., 1.],
                            [6., 5., 4., 3., 2.],
                            [7., 6., 5., 4., 3.],
                            [8., 7., 6., 5., 4.]]),
            index   = np.array([5, 6, 7, 8, 9]),
            columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
        ).assign(
            exog_1=pd.Categorical( range(5, 10), categories=range(10)),
            exog_2=pd.Categorical( range(105, 110), categories=range(100, 110))
        ),
        pd.Series(
            np.array([5, 6, 7, 8, 9]),
            index = np.array([5, 6, 7, 8, 9]),
            name = 'y'
        )
    )          

    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_exception_when_exog_is_categorical_of_no_int():
    """
    Test exception is raised when exog is categorical with no int values.
    """
    y = pd.Series(np.arange(3))
    exog = pd.Series(['A', 'B', 'C'], name='exog', dtype='category')
    forecaster = ForecasterAutoreg(LinearRegression(), lags=2)
    err_msg = re.escape(
                ('If exog is of type category, it must contain only integer values. '
                 'See skforecast docs for more info about how to include categorical features '
                 'https://joaquinamatrodrigo.github.io/skforecast/latest/user_guides/'
                 'categorical-features.html')  
              )
    with pytest.raises(TypeError, match = err_msg):
        forecaster.create_train_X_y(y=y, exog=exog)


def test_create_train_X_y_warning_when_exog_has_missing_values():
    """
    Test exception is issues a warning when exog has missing values.
    """
    y = pd.Series(np.arange(4))
    exog = pd.Series([1, 2, 3, np.nan], name='exog')
    forecaster = ForecasterAutoreg(LinearRegression(), lags=2)
    warn_msg = re.escape(
                ('`exog` has missing values. Most of machine learning models do '
                 'not allow missing values. Fitting the forecaster may fail.')  
              )
    with pytest.warns(MissingValuesExogWarning, match = warn_msg):
        forecaster.create_train_X_y(y=y, exog=exog)


@pytest.mark.parametrize("y                        , exog", 
                         [(pd.Series(np.arange(50)), pd.Series(np.arange(10))), 
                          (pd.Series(np.arange(10)), pd.Series(np.arange(50))), 
                          (pd.Series(np.arange(10)), pd.DataFrame(np.arange(50).reshape(25,2)))])
def test_create_train_X_y_exception_when_len_y_is_different_from_len_exog(y, exog):
    """
    Test exception is raised when length of y is not equal to length exog.
    """
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)
    err_msg = re.escape(
                (f'`exog` must have same number of samples as `y`. '
                 f'length `exog`: ({len(exog)}), length `y`: ({len(y)})')
              )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.create_train_X_y(y=y, exog=exog)

  
def test_create_train_X_y_exception_when_y_and_exog_have_different_index():
    """
    Test exception is raised when y and exog have different index.
    """
    forecaster = ForecasterAutoreg(LinearRegression(), lags=5)

    err_msg = re.escape(
                ('Different index for `y` and `exog`. They must be equal '
                 'to ensure the correct alignment of values.')  
              )
    with pytest.raises(ValueError, match = err_msg):
        forecaster.fit(
            y=pd.Series(np.arange(10), index=pd.date_range(start='2022-01-01', periods=10, freq='1D')),
            exog=pd.Series(np.arange(10), index=pd.RangeIndex(start=0, stop=10, step=1))
        )    


def test_create_train_X_y_output_when_exog_is_None_and_transformer_exog_is_not_None():
    """
    Test the output of create_train_X_y when exog is None and transformer_exog
    is not None.
    """
    forecaster = ForecasterAutoreg(
        regressor = LinearRegression(),
        lags = 5,
        transformer_exog = StandardScaler()
    )

    results = forecaster.create_train_X_y(y=pd.Series(np.arange(10)))
    expected = (pd.DataFrame(
                    data = np.array([[4., 3., 2., 1., 0.],
                                     [5., 4., 3., 2., 1.],
                                     [6., 5., 4., 3., 2.],
                                     [7., 6., 5., 4., 3.],
                                     [8., 7., 6., 5., 4.]]),
                    index   = pd.RangeIndex(start=5, stop=10, step=1),
                    columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
                ),
                pd.Series(
                    np.array([5, 6, 7, 8, 9]),
                    index = pd.RangeIndex(start=5, stop=10, step=1),
                    name = 'y'
                ))
    
    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_y_is_series_10_and_transformer_y_is_StandardScaler():
    """
    Test the output of create_train_X_y when exog is None and transformer_exog
    is not None.
    """
    forecaster = ForecasterAutoreg(
                    regressor = LinearRegression(),
                    lags = 5,
                    transformer_y = StandardScaler()
                )

    results = forecaster.create_train_X_y(y=pd.Series(np.arange(10)))
    expected = (pd.DataFrame(
                    data = np.array([[-0.17407766, -0.52223297, -0.87038828, -1.21854359, -1.5666989 ],
                                     [0.17407766, -0.17407766, -0.52223297, -0.87038828, -1.21854359],
                                     [0.52223297,  0.17407766, -0.17407766, -0.52223297, -0.87038828],
                                     [0.87038828,  0.52223297,  0.17407766, -0.17407766, -0.52223297],
                                     [1.21854359,  0.87038828,  0.52223297,  0.17407766, -0.17407766]]),
                    index   = pd.RangeIndex(start=5, stop=10, step=1),
                    columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5']
                ),
                pd.Series(
                    np.array([0.17407766, 0.52223297, 0.87038828, 1.21854359, 1.5666989]),
                    index = pd.RangeIndex(start=5, stop=10, step=1),
                    name = 'y'
                ))

    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])


def test_create_train_X_y_output_when_transformer_y_and_transformer_exog():
    """
    Test the output of create_train_X_y when using transformer_y and transformer_exog.
    """
    y = pd.Series(np.arange(8))
    exog = pd.DataFrame({
                'col_1': [7.5, 24.4, 60.3, 57.3, 50.7, 41.4, 87.2, 47.4],
                'col_2': ['a', 'a', 'a', 'a', 'b', 'b', 'b', 'b']
            })

    transformer_y = StandardScaler()
    transformer_exog = ColumnTransformer(
                            [('scale', StandardScaler(), ['col_1']),
                             ('onehot', OneHotEncoder(), ['col_2'])],
                            remainder = 'passthrough',
                            verbose_feature_names_out = False
                        )

    forecaster = ForecasterAutoreg(
                    regressor = LinearRegression(),
                    lags = 5,
                    transformer_y = transformer_y,
                    transformer_exog= transformer_exog
                )

    expected = (pd.DataFrame(
                    data = np.array([[0.21821789, -0.21821789, -0.65465367, -1.09108945,
                                     -1.52752523, -0.25107995,  0.        ,  1.        ],
                                     [0.65465367,  0.21821789, -0.21821789, -0.65465367,
                                      -1.09108945, 1.79326881,  0.        ,  1.        ],
                                     [1.09108945,  0.65465367,  0.21821789, -0.21821789,
                                      -0.65465367, 0.01673866,  0.        ,  1.        ]]),
                    index   = pd.RangeIndex(start=5, stop=8, step=1),
                    columns = ['lag_1', 'lag_2', 'lag_3', 'lag_4', 'lag_5', 'col_1',
                               'col_2_a', 'col_2_b']
                ),
                pd.Series(
                    np.array([0.65465367, 1.09108945, 1.52752523]),
                    index = pd.RangeIndex(start=5, stop=8, step=1),
                    name = 'y'
                ))

    results = forecaster.create_train_X_y(y=y, exog=exog)

    pd.testing.assert_frame_equal(results[0], expected[0])
    pd.testing.assert_series_equal(results[1], expected[1])