import React, { useEffect, useState } from 'react';
import Autosuggest from 'react-autosuggest';
import ReactSelect from 'react-select';
import { FetchError, Filter, FilterOptions, Searchable } from '../types';
import { DropdownIndicator, unfocusALl, useKeyPress } from '../utils';
import './index.scss';

export const SearchBar = ({
    fetchCallback,
    renderSuggestionCallback,
    getSuggestionValueCallback,
    searchCompleted,
    filters,
    changeFilters,
}: {
    fetchCallback: (s: string, f?: Filter[]) => Promise<Searchable[] | FetchError>;
    renderSuggestionCallback: (s: Searchable) => JSX.Element;
    getSuggestionValueCallback: (s: Searchable) => string;
    searchCompleted: (v: string, filters?: Filter[]) => void;
    filters?: Filter[];
    changeFilters?: (nf: string[]) => void;
}) => {
    const [suggestions, setSuggestions] = useState<Searchable[]>([]);
    const [autosuggestValue, setAutosuggestValue] = useState<string>('');
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const enterPress = useKeyPress('Enter');
    const [showFilters, setShowFilters] = useState<boolean>(!!filters); // not an emphasis :)
    const [callbackFilters, setCallbackFilters] = useState<Filter[]>(filters || []);

    useEffect(() => {
        if (enterPress) {
            unfocusALl();
            if (showFilters) searchCompleted(autosuggestValue, callbackFilters);
            else searchCompleted(autosuggestValue);
        }
    }, [enterPress]);

    useEffect(() => {
        setCallbackFilters(filters || []);
    }, [filters]);

    const loadSuggestions = (value: string) => {
        setIsLoading(true);
        fetchCallback(value, filters).then(resp => {
            if ((resp as FetchError).error) {
                console.log((resp as FetchError).error.status);
                setIsLoading(false);
                return;
            }
            setSuggestions(resp as Searchable[]);
            setIsLoading(false);
        });
    };

    const onChange = (event: React.FormEvent<HTMLElement>, { newValue }: { newValue: string }) => {
        setAutosuggestValue(newValue);
    };

    const onSuggestionsFetchRequested = ({ value }: { value: string }) => {
        loadSuggestions(value);
    };

    const onSuggestionsClearRequested = () => {
        setSuggestions([]);
    };

    const inputProps = {
        placeholder: 'Start typing...',
        value: autosuggestValue,
        onChange: onChange,
    };

    const onSuggestionSelected = () => {
        setAutosuggestValue('');
    };

    const updateFilters = (el: Filter, newFilter: FilterOptions) => {
        const a: Filter = {
            name: el.name,
            options: el.options,
            defaultValue: el.defaultValue,
            value: newFilter,
        };
        for (let el of callbackFilters) {
            if (el.name === a.name) el.value = a.value;
        }
        setCallbackFilters(callbackFilters);
    };

    return (
        <div className="searchbar">
            <div className="searchbar-container">
                <Autosuggest
                    suggestions={suggestions}
                    onSuggestionsFetchRequested={onSuggestionsFetchRequested}
                    onSuggestionsClearRequested={onSuggestionsClearRequested}
                    getSuggestionValue={getSuggestionValueCallback}
                    renderSuggestion={renderSuggestionCallback}
                    onSuggestionSelected={onSuggestionSelected}
                    focusInputOnSuggestionClick={false}
                    inputProps={inputProps}
                />
                <div
                    className="searchbar-container__button"
                    onClick={() => {
                        if (showFilters) searchCompleted(autosuggestValue, callbackFilters);
                        else searchCompleted(autosuggestValue);
                    }}>
                    <span className="text-18 font-ptmono weight-400 searchbar-container__button_text">
                        SEARCH
                    </span>
                </div>
            </div>
            {showFilters && filters ? (
                <div className="searchbar-filters">
                    {filters.map(el => (
                        <div className="searchbar-filters__item">
                            <span className="text-18 font-ptmono weight-700 searchbar-filters__item_filtername">
                                {el.name}:
                            </span>
                            <ReactSelect
                                isSearchable={false}
                                options={el.options}
                                components={{ DropdownIndicator }}
                                defaultValue={el.value ? el.value : el.defaultValue}
                                onChange={(v: unknown) => {
                                    // onChange have some very funky description - (newValue: unknown, actionMeta: ActionMeta<unknown>) => void
                                    updateFilters(el, v as FilterOptions);
                                }}
                            />
                        </div>
                    ))}
                </div>
            ) : (
                <></>
            )}
        </div>
    );
};
