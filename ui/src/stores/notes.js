import { defineStore } from "pinia";
import axios from "axios";

export const useNotesStore = defineStore({
  id: "notes",
  state: () => ({
    notes: null,
    note: null,
  }),
  getters: {
    // doubleCount: (state) => state.counter * 2,
    stateNotes: (state) => state.notes,
    stateNote: (state) => state.note,
  },
  actions: {
    async createNote({ dispatch }, note) {
      await axios.post("notes", note);
      await dispatch("getNotes");
    },
    async getNotes({ commit }) {
      let { data } = await axios.get("notes");
      commit("setNotes", data);
    },
    async viewNote({ commit }, id) {
      let { data } = await axios.get(`note/${id}`);
      commit("setNote", data);
    },
    // eslint-disable-next-line no-empty-pattern
    async updateNote({}, note) {
      await axios.patch(`note/${note.id}`, note.form);
    },
    // eslint-disable-next-line no-empty-pattern
    async deleteNote({}, id) {
      await axios.delete(`note/${id}`);
    },
  },
  mutations: {
    setNotes(state, notes) {
      state.notes = notes;
    },
    setNote(state, note) {
      state.note = note;
    },
  },
});
