from typing import List


class Key:
    def __init__(self, table_or_path, id_or_name=None, namespace=""):
        """
            table_or_path is either a string kind (e.g. 'my_table') or a path
            (e.g. ['collectionA', 1234, 'collectionB']). If it's a path the number
            of elements should be odd (because id_or_name would be the final identifier)
        """
        self.path = table_or_path if isinstance(table_or_path, (list, tuple)) else [table_or_path]
        self.id_or_name = id_or_name
        self.namespace = namespace or ""  # Make sure if someone passes None we normalize to "" consistently

    def ancestor(self):
        # A path is the lead up to the id. So an ancestor would have [kind, id, kind] at least.
        if len(self.path) >= 3:
            return Key(
                table_or_path=self.path[:-2],
                id_or_name=self.path[-2],
                namespace=self.namespace
            )

    def complete_key(self, id_or_name):
        if self.id_or_name is not None:
            raise ValueError("Attempted to complete a complete key")

        self.id_or_name = id_or_name

    def is_partial(self) -> bool:
        return self.id_or_name is None

    def __repr__(self) -> str:
        return 'Key<{}, {}, namespace={}>'.format(
            ", ".join([str(x) for x in self.path]), self.id_or_name, self.namespace
        )

    def __eq__(self, other) -> bool:
        if other is None:
            return False

        if not isinstance(other, Key):
            return NotImplemented

        return self.path == other.path and self.id_or_name == other.id_or_name

    def __hash__(self):
        return hash(tuple(list(self.path) + [self.id_or_name]))

    def __lt__(self, other) -> bool:
        def cmp(a, b) -> bool:
            if a is None and b is None:
                return False

            if a is None:
                return True

            if b is None:
                return False

            return a < b

        lhs_args = [self.namespace] + list(self.path)
        if self.is_partial():
            # If the key is partial, then we need to add a blank placeholder
            # for the id or name so we can compare correctly
            lhs_args.append("")
        else:
            lhs_args.append(self.id_or_name)

        rhs_args = [other.namespace] + list(other.path)
        if other.is_partial():
            rhs_args.append("")
        else:
            rhs_args.append(other.id_or_name)

        # If things are equal, they are not less
        if lhs_args == rhs_args:
            return False

        for lhs_component, rhs_component in zip(lhs_args, rhs_args):
            # If any of the lhs components are less than the rhs components
            # then return True, they may be equal if this is False and so
            # we continue on
            comparison = cmp(lhs_component, rhs_component)
            if comparison:
                return True

        # lhs might be shorter, but equivalent up to that point. In that case lhs
        # is classes as less
        if len(lhs_args) < len(rhs_args) and lhs_args == rhs_args[len(lhs_args):]:
            return True

        return False


class Entity:
    """
        Represents an entity / row returned from a non-relational backend.
    """

    def __init__(self, key, properties=None, exclude_from_indexes=None):
        assert (key)
        self._key = key
        self._properties = properties or {}
        self._properties_to_unindex = set()
        self._properties_to_exclude_from_index = set(exclude_from_indexes) if exclude_from_indexes else set()

    def set_key(self, key: Key):
        assert (key)
        self._key = key

    def key(self) -> Key:
        return self._key

    def keys(self) -> List[str]:
        return [str(k) for k, v in self._properties.items()]

    def get(self, key, default=None):
        return self._properties.get(key, default)

    def update(self, entity):
        if entity.key().id_or_name and not self.key().id_or_name:
            # We do this to catch accidental errors, it's fine to update an entity
            # with an existing key with new data, but if we're updating one without
            # a key, from one with a key, then something is probably wrong somewhere
            raise ValueError(
                "Tried to update an entity without a key, with one with a key"
            )

        self._properties.update(entity._properties)

        # We set the excluded properties as the superset of both entities (which is comparable to
        # make the fields the superset of all fields). This protects us against problems
        # during update where a new TextField might have been added to the model and we need
        # to include that in the updated entity (E.g. we can't just rely on what the database
        # gives us back)
        self._properties_to_exclude_from_index = self._properties_to_exclude_from_index.union(
            entity._properties_to_exclude_from_index
        )

    def __getitem__(self, key):
        return self._properties[key]

    def __setitem__(self, key, value):
        self._properties[key] = value

    def __delitem__(self, key):
        del self._properties[key]

    def add_property_to_unindex(self, property):
        self._properties_to_unindex.add(property)

    def less_than(self, other, orderings, key_property_name) -> bool:
        """
            Returns True if self < other when compared on the specified
            field orderings (format: ["field", "-field"])
        """
        for field in orderings:
            descending = field.startswith("-")
            field = field.lstrip("-")

            if field == key_property_name:
                lhs_value = self.key()
                rhs_value = other.key()
            else:
                lhs_value = self.get(field)
                rhs_value = other.get(field)

            if isinstance(lhs_value, list):
                lhs_value = min(lhs_value) if lhs_value else None

            if isinstance(rhs_value, list):
                rhs_value = min(rhs_value) if rhs_value else None

            # If we're descending, swap the values before
            # we do any checking
            if descending:
                lhs_value, rhs_value = rhs_value, lhs_value

            if lhs_value is None and rhs_value is None:
                less = False
            elif lhs_value is None and rhs_value is not None:
                less = True
            elif lhs_value is not None and rhs_value is None:
                return False
            else:
                less = lhs_value < rhs_value

            if less:
                return True

        return False
